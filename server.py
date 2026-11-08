"""Web server for the study assistant: a chat page plus a chat bubble for Moodle.

Run:  python server.py
  Chat page:       http://localhost:8000/
  Moodle bubble:   add  <script src="http://localhost:8000/embed.js"></script>
                   to Site administration > Appearance > Additional HTML > "Before BODY is closed".

Prototype note: every chat uses the one student token in .env (MOODLE_TOKEN), so everyone
sees that student's data. Real per-student sign-in would come from Moodle via LTI 1.3.
"""

import os
import threading
import uuid
from pathlib import Path

import anthropic
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel

import agent  # loads .env
from lms import make_lms

WEB = Path(__file__).with_name("web")
MAX_SESSIONS = 200

app = FastAPI(title="Study Assistant")
client = anthropic.Anthropic()
lms, source = make_lms()

# In-memory chat histories, one per browser session. Restarting the server clears them.
sessions: dict[str, list] = {}
locks: dict[str, threading.Lock] = {}
sessions_lock = threading.Lock()


class ChatIn(BaseModel):
    session_id: str | None = None
    message: str


class ChatOut(BaseModel):
    session_id: str
    reply: str
    looked_up: list[str]


@app.get("/")
def chat_page():
    return FileResponse(WEB / "chat.html")


@app.get("/embed.js")
def embed_js():
    # Short cache so edits show up in Moodle after a reload.
    return Response((WEB / "embed.js").read_text(), media_type="application/javascript",
                    headers={"Cache-Control": "max-age=60"})


@app.get("/api/health")
def health():
    return {"ok": True, "lms": source}


@app.post("/api/chat", response_model=ChatOut)
def chat(body: ChatIn):
    text = body.message.strip()
    if not text:
        raise HTTPException(400, "Empty message")
    if len(text) > 4000:
        raise HTTPException(400, "Message too long")

    with sessions_lock:
        sid = body.session_id if body.session_id in sessions else str(uuid.uuid4())
        if sid not in sessions:
            if len(sessions) >= MAX_SESSIONS:  # drop the oldest chat
                old = next(iter(sessions))
                sessions.pop(old)
                locks.pop(old, None)
            sessions[sid] = []
            locks[sid] = threading.Lock()
        messages, lock = sessions[sid], locks[sid]

    looked_up: list[str] = []
    with lock:  # one turn at a time per chat
        start = len(messages)
        messages.append({"role": "user", "content": text})
        try:
            reply = agent.ask(
                client, lms, messages,
                on_tool=lambda name, args: looked_up.append(name),
                approve=lambda name, args: False,  # no approval UI on the web yet
            )
        except anthropic.RateLimitError:
            del messages[start:]
            raise HTTPException(429, "The assistant is busy. Try again in a moment.")
        except (anthropic.APIStatusError, anthropic.APIConnectionError) as e:
            del messages[start:]
            raise HTTPException(502, f"The assistant had a problem reaching Claude: {type(e).__name__}")
    return ChatOut(session_id=sid, reply=reply or "(no reply)", looked_up=looked_up)


@app.post("/api/reset")
def reset(body: ChatIn):
    with sessions_lock:
        sessions.pop(body.session_id or "", None)
        locks.pop(body.session_id or "", None)
    return {"ok": True}


if __name__ == "__main__":
    host = os.getenv("AGENT_HOST", "127.0.0.1")  # set 0.0.0.0 to let teammates connect
    port = int(os.getenv("AGENT_PORT", "8000"))
    print(f"Study assistant web server using {source}")
    print(f"Chat page: http://localhost:{port}/   Moodle bubble script: http://localhost:{port}/embed.js")
    uvicorn.run(app, host=host, port=port)
