"""A student-facing study assistant for an LMS, powered by Claude.

Run:  python agent.py
Ask things like "What's due this week?", "How am I doing in CS101?",
or "Explain the Lab 1 instructions, I don't get what a loop counter is."
"""

import json
from datetime import date

import anthropic
from dotenv import load_dotenv

from lms import make_lms

load_dotenv()

MODEL = "claude-opus-5-5"

SYSTEM = """You are a friendly study assistant for a student, connected to their courses in the school's LMS.

What you do:
- Help them stay organized: what's due, what's missing, their current grades, recent announcements.
- Answer questions about their courses using the real course material (syllabus, pages, assignment instructions).
  Look things up with the tools before answering; never invent due dates, grades or policies.
  If you can't find something, say so and suggest they ask their instructor.
- Tutor them: explain concepts, give examples, check their reasoning, and quiz them when they're studying.

Academic integrity:
- Don't do graded work for them. For an assignment, quiz or exam, don't write the answers, code or essay they'll submit.
  Instead explain the idea, work a *different* similar example, ask guiding questions, or give feedback on their own attempt.
- If the syllabus has rules about AI tools, follow them.

Style: short, encouraging, plain language. Use lists for dates and to-dos.

Today is {today}."""

# Tool definitions Claude sees. Each name maps to a method on the LMS client.
_COURSE = {"course_id": {"type": "integer"}}
TOOLS = [
    {
        "name": "list_my_courses",
        "description": "List the student's active courses with ids and their current overall score/grade.",
        "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "list_my_assignments",
        "description": "List a course's assignments with due dates and the student's own status, grade, and late/missing flags.",
        "input_schema": {"type": "object", "properties": _COURSE, "required": ["course_id"], "additionalProperties": False},
    },
    {
        "name": "get_assignment",
        "description": "Get one assignment's full instructions.",
        "input_schema": {
            "type": "object",
            "properties": {**_COURSE, "assignment_id": {"type": "integer"}},
            "required": ["course_id", "assignment_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "get_syllabus",
        "description": "Get the course summary/syllabus: policies, grading, late rules, office hours. If it's thin, look for a Syllabus page via list_modules.",
        "input_schema": {"type": "object", "properties": _COURSE, "required": ["course_id"], "additionalProperties": False},
    },
    {
        "name": "list_modules",
        "description": "List the course's sections/modules and their items. Page items include a page_id for get_page.",
        "input_schema": {"type": "object", "properties": _COURSE, "required": ["course_id"], "additionalProperties": False},
    },
    {
        "name": "get_page",
        "description": "Read a course content page (lecture notes, readings, sometimes the syllabus) by its page_id from list_modules.",
        "input_schema": {
            "type": "object",
            "properties": {**_COURSE, "page_id": {"type": "string"}},
            "required": ["course_id", "page_id"],
            "additionalProperties": False,
        },
    },
    {
        "name": "list_announcements",
        "description": "List the course's most recent announcements from the instructor.",
        "input_schema": {"type": "object", "properties": _COURSE, "required": ["course_id"], "additionalProperties": False},
    },
]
for t in TOOLS:
    t["strict"] = True

# Tools that change things in the LMS need a human's OK. The student tools are all read-only today;
# add a name here if you give the agent a write tool (e.g. submitting work or messaging an instructor).
NEEDS_APPROVAL: set[str] = set()


def run_tool(lms, name: str, args: dict) -> tuple[str, bool]:
    """Execute one tool call. Returns (result_text, is_error)."""
    if name not in {t["name"] for t in TOOLS}:
        return f"Unknown tool {name}", True
    if name in NEEDS_APPROVAL:
        print(f"\n--- The assistant wants to {name} ---\n{json.dumps(args, indent=2)}")
        if input("Approve? [y/N] ").strip().lower() != "y":
            return "The user declined this action. Ask what they'd like changed.", True
    try:
        result = getattr(lms, name)(**args)
        return json.dumps(result, default=str), False
    except Exception as e:  # surface LMS/HTTP errors to Claude so it can recover
        return f"Error: {e}", True


def ask(client, lms, messages: list) -> None:
    """Run the agent loop for one user turn, appending everything to `messages`."""
    while True:
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=SYSTEM.format(today=date.today().strftime("%A, %B %d, %Y")),
            tools=TOOLS,
            messages=messages,
            output_config={"effort": "medium"},
            # If a safety classifier declines, the API retries on a suitable model automatically.
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
        # Append the full content (not just text) so the conversation stays valid.
        messages.append({"role": "assistant", "content": response.content})

        for block in response.content:
            if block.type == "text" and block.text.strip():
                print(f"\nAssistant: {block.text}")

        if response.stop_reason == "refusal":
            print("\n(The request was declined.)")
            return
        if response.stop_reason == "max_tokens":
            print("\n(Response was cut off at max_tokens.)")
            return
        if response.stop_reason == "pause_turn":
            continue
        if response.stop_reason != "tool_use":
            return

        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  [looking up] {block.name}({json.dumps(block.input)})")
                text, is_error = run_tool(lms, block.name, block.input)
                results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": text, "is_error": is_error}
                )
        # All results go back in a single user message.
        messages.append({"role": "user", "content": results})


def main():
    client = anthropic.Anthropic()
    lms, source = make_lms()
    print(f"Study assistant ready, using {source}. Type 'quit' to exit.")
    messages: list = []
    while True:
        try:
            user = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user.lower() in {"quit", "exit"}:
            break
        if not user:
            continue
        start = len(messages)
        messages.append({"role": "user", "content": user})
        try:
            ask(client, lms, messages)
        except anthropic.AuthenticationError:
            print("Auth failed: set ANTHROPIC_API_KEY in .env")
            del messages[start:]  # drop the failed turn so history stays valid
        except anthropic.RateLimitError:
            print("Rate limited, wait a moment and try again.")
            del messages[start:]
        except anthropic.APIStatusError as e:
            print(f"API error {e.status_code}: {e.message}")
            del messages[start:]
        except anthropic.APIConnectionError:
            print("Couldn't reach the Claude API. Check your connection.")
            del messages[start:]


if __name__ == "__main__":
    main()
