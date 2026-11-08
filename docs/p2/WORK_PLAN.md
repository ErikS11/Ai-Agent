# P2 Work Plan: Group 1, LMS AI Agent

**Due: Sunday, Nov 8, 2026, 11:59 PM Central.** No late work.
Read [ONBOARDING.md](../../ONBOARDING.md) first. It explains what has been built and how to set it up.

## How the grade works, and the one rule that matters most

60 points: 48 for the team document and **12 for each person's own evidence**. That individual score only counts work a grader can open in this repository:

| Your score | What the repo must show |
|---|---|
| **12** | You own specific sections, **your own commits / PR** before the deadline, **and you reviewed at least one teammate's PR** |
| 9 | Own commits, but no review |
| 4 | You claim work, but there's nothing in the repo |

We lost a lot in P1 (C4: 3/6, C5: 4/8 for everyone) because the repo was empty. So:

1. **Commit your own section from your own GitHub account**, on a branch, through a **pull request (PR)**: a request on GitHub to merge your branch into `main` after a teammate approves it. Step-by-step instructions are in ONBOARDING.md, section 2, step 6.
2. **Review the PR you are assigned below** (approve it or request changes on GitHub).
3. Draft together in our shared doc if you like, but **the final text of your section is committed by you.**

## Who does what

Each person owns sections worth roughly the same effort. Roles carry over from P1.

| Member | P1 role | P2 sections you own | Reviews PR of |
|---|---|---|---|
| **John** | Team Lead | **0** (0.1 contribution record, 0.2 changes since P1), **1** update, **10** (plan to P3, risks, repo, AI-use table), **11** open questions, **12** baseline. Assembles the final PDF, commits it to `/docs/p2`, tags `p2`, uploads to Canvas | Erik |
| **Erik** | Requirements Engineer & Use Case Analyst | **3** update (fix QR-02, reconcile UC IDs, CON-01 to Moodle, no "pending" sources) and **4** use-case analysis: 4.1 selection, 4.2 three expanded use cases, 4.3 self-review log | Omor |
| **Omor** | QA Tester | **5.1** domain model (diagram + table), **5.2** object interaction for **UC-01** (non-trivial steps, scenario table, analysis sequence diagram), **5.3** cross-checks K1 to K6 (run last, across everyone's work) | Daniel |
| **Daniel** | Product Manager / UI | **5.2** object interaction for **UC-02** (non-trivial steps, scenario table, analysis sequence diagram), **7** design rationale: at least 3 ADRs (ADR-01 = style, agreed with Ahmad) + 7.2 trade-off summary | Ahmad |
| **Ahmad** | System Architect | **6** high-level design: 6.1 three QAS with numbers, 6.2 style + 2 rejected alternatives, 6.3 component view, 6.4 UML deployment view, 6.5 analysis-to-component mapping, 6.6 design principles | Zaid |
| **Zaid** | Requirements & Feasibility Analyst | **2** update (stakeholder evidence via a short student survey, feasibility verdicts backed by evidence), **8** architecture spike in `/spikes/S-01-.../` with measured numbers, **9** traceability matrix + gap analysis | John |

Omor co-wrote section 2 in P1. Zaid owns it now, so if Omor helps with the survey, record that in 0.1.

## Answering every point of the P1 feedback (goes in 0.2, owned by John)

| Feedback point | What we do | Owner |
|---|---|---|
| C4: repo had no commits; branching, PR and issue conventions not verifiable | Every section goes through a PR with a review. Each person's 0.1 row cites real commit hashes and PR numbers | Everyone, John records it |
| C1: stakeholder needs in 2.2 are assumptions | Short student survey (Google Form, 5 questions, aim for 10+ classmates by Sunday noon). Report numbers in 2.2 | Zaid (Omor may help) |
| C1: feasibility verdicts conditional, no evidence | We now have **a working call against a self-hosted LMS API**: Moodle runs locally and the agent reads courses, assignments, grades, pages and announcements through it (see repo history). Cite the commits | Zaid |
| C3: matrix says UC-03 and UC-05, diagram shows UC-01 to UC-04 (UC-04 = practice questions) | Settle one UC list in 3.4, use the same IDs everywhere, and mark anything dropped as "Withdrawn (CH-nn)" | Erik |
| C3: QR-02 is not testable | Reword with a task, a population, a threshold and a time limit | Erik |
| Contribution table says "repository links to be added" | Real links in 0.1 | John |
| (Our own change) Canvas → Moodle | Canvas Lite blocks API tokens for every account, so the agent could not connect. We switched to self-hosted Moodle 5.3. Changes CON-01, answers Q1, affects 1.1/1.3 wording | John records it, Erik updates 3.3 |

## Shared numbering, so six people don't collide

| ID type | Who assigns | Range |
|---|---|---|
| CH-nn (changes, 0.2) | John | CH-01 to CH-20. Ask John for a number |
| UC-nn | Erik | Final list published in the team chat by **Sat 11 PM** |
| QAS-nn | Ahmad | QAS-01 to QAS-05 |
| ADR-nn | Daniel | ADR-01 is the style (from Ahmad's 6.2). ADR-02 onward are Daniel's |
| S-nn (spike) | Zaid | S-01 |
| R-n (risks) | John | Keep R1 to R5, new risks start at R6 |
| Q-n (questions) | John | Keep Q1 to Q3, new ones start at Q4 |

## Timeline (tonight and tomorrow)

| When | Done when | Who |
|---|---|---|
| **Sat 11 PM** | Everyone has cloned the repo and can push a branch. Erik posts the final UC list. Zaid's survey is out. Ahmad posts the draft component list | All |
| **Sun 10 AM** | Erik's 4.2 drafts are in the shared doc, so Omor and Daniel can build scenario tables from them. Omor's domain model draft is shared | Erik, Omor |
| **Sun 1 PM** | Ahmad's 6.2 style is decided, so Daniel can write ADR-01. Zaid's spike has measured numbers | Ahmad, Zaid, Daniel |
| **Sun 4 PM** | **Every owner has opened their PR** | All |
| **Sun 6 PM** | **Every PR is reviewed and merged** (use the review pairs above) | All |
| **Sun 7 PM** | Omor runs cross-checks K1 to K6 across everyone's work. Zaid finishes 9 (traceability needs all the IDs). John fills 0.1 with real hashes and PR numbers | Omor, Zaid, John |
| **Sun 9 PM** | John assembles the PDF and removes every guidance, example and warning box plus the two marking pages. Everyone signs section 12 | John, all |
| **Sun 10:30 PM** | PDF committed to `/docs/p2`, tag `p2` on that commit, `git push origin p2` | John |
| **Sun 11 PM** | **One** upload to Canvas (John only) | John |

## Where files go

```
docs/p2/sections/0-records.md        John
docs/p2/sections/1-introduction.md   John
docs/p2/sections/2-overall.md        Zaid
docs/p2/sections/3-requirements.md   Erik
docs/p2/sections/4-use-cases.md      Erik
docs/p2/sections/5-1-domain.md       Omor
docs/p2/sections/5-2-uc01.md         Omor
docs/p2/sections/5-2-uc02.md         Daniel
docs/p2/sections/5-3-crosscheck.md   Omor
docs/p2/sections/6-design.md         Ahmad
docs/p2/sections/7-rationale.md      Daniel
docs/p2/sections/8-spike.md          Zaid
docs/p2/sections/9-traceability.md   Zaid
docs/p2/sections/10-12-plan.md       John
docs/p2/diagrams/                    every diagram's source file (draw.io / PlantUML) + exported PNG
spikes/S-01-<short-name>/            Zaid's spike code, raw results, README
docs/p2/CS3354_P2_Group1.pdf         final PDF (John, Sunday night)
```

Diagram tools: draw.io (diagrams.net) or PlantUML. **Commit the source file**, not just the image.

## Facts every author should use (so the sections agree with each other and with the code)

**What exists now.** These are real and in the repo, so cite them:

- **Moodle 5.3** (open-source LMS) runs in Docker with PostgreSQL. It has a sample course CS101 and a test student.
- **Agent core** (`agent.py`): sends the student's question to the Claude model with 7 **read-only** tools. Claude decides which to call, the agent runs them, and it loops until Claude answers. The system prompt makes it a tutor that won't do graded work.
- **LMS adapter** (`lms.py`): turns tool calls into Moodle web-service calls using the **student's own token**, so it only sees what that student can see. `MockLMS` gives the same answers from a file for offline testing.
- **Agent server** (`server.py`): web API (`/api/chat`) plus the chat page.
- **Chat UI** (`web/chat.html`) and the **Moodle chat bubble** (`web/embed.js`, injected through Moodle's Additional HTML).
- **External system:** Anthropic Claude API (HTTPS). Student data in a question leaves our host here. That's a trust boundary and a FERPA point.

**The 7 tools:** list my courses (with grade), list my assignments (due date, status, grade, late, missing), get assignment instructions, get syllabus/course summary, list modules, get page, list announcements.

**Real alternatives the team already weighed** (good ADR material, because they actually happened):

- LMS: Canvas Lite (blocked: no API tokens) vs Google Classroom (needs a Google Cloud OAuth app) vs **self-hosted Moodle (chosen)**.
- How the agent gets course data: **LLM tool-calling on demand (chosen)** vs pre-loading all course content into the prompt vs a search index (RAG).
- How students reach it: terminal app vs standalone web page vs **chat bubble inside Moodle (chosen)** vs a Moodle plugin.
- Student identity: **one student's token from config (prototype, chosen for now)** vs per-student token pasted in vs **LTI 1.3 launch from Moodle (planned for P3)**.

**Known gaps to name honestly** (sections 9.2 and 11):

- UC-01 promises "a source reference" with each answer. The agent doesn't cite sources yet.
- FR-06 (due within 7 days) works because Claude reads the dates. There's no dedicated filter, and assignments are fetched one course at a time.
- QR-01 (95% under 5 s) has **not been measured**. Each answer makes several model and tool calls, so it's the riskiest requirement. **That makes it a good spike.**
- QR-03 (deny unauthorized users) depends on identity, which is still a single test token in the prototype.
- CON / 2.4 said campus SSO with Duo. The prototype uses Moodle tokens, and LTI 1.3 is the planned path.

**Suggested spike (Zaid):** *S-01: Can the agent answer a typical student question within 5 s at the 95th percentile with 20 concurrent users (QR-01)?* Send 100 questions (20 at a time) to `POST /api/chat` on the running server, record each response time, and report p50/p95. If it fails, that's still a valid result. It feeds an ADR (for example lower effort, a smaller model, streaming, or relaxing QR-01). Cost: a few dollars of API credit. Use the mock LMS or Moodle, but say which.

## After P2: what we build in P3

These are not part of P2 (P2 forbids production code beyond the spike). This is the backlog so everyone has a build area next:

| Member | Build area (P3) | Requirement |
|---|---|---|
| John | Per-student sign-in through **LTI 1.3** (Moodle launches the agent with the student's identity) | QR-03, 2.4 SSO |
| Erik | **Source references** in every answer (page / assignment the answer came from) | FR-03, UC-01 |
| Omor | **Accuracy evaluation set**: 100 questions + answer key, script that scores the agent | QR-04, R2 |
| Daniel | **Chat UI polish + accessibility** (keyboard, screen reader, mobile), loading CS 3354 sample content into Moodle | 2.3, 2.4, R3 |
| Ahmad | **Cross-course "what's due"** tool with a 7-day flag + latency fixes from the spike | FR-04 to FR-06, QR-01 |
| Zaid | **Practice-question mode** (FR-08) and LMS-failure handling with clear messages | FR-08, FR-07 |

## Before John submits (checklist from the brief)

- [ ] Every P1 feedback point answered in 0.2
- [ ] Every guidance, example and warning box, every `[placeholder]`, and both marking pages removed
- [ ] Section numbering exactly as the template
- [ ] 3+ use cases expanded; 2 carried through scenario tables + sequence diagrams
- [ ] Every QAS has a number in its response measure
- [ ] Every component answers to a UC, QAS or ADR
- [ ] Spike + README + numbers in `/spikes`
- [ ] Every commit / PR cited in 0.1 exists and was pushed before 11:59 PM
- [ ] No API keys or passwords in the repo (`.env` is git-ignored, so keep it that way)
- [ ] Repo is public
- [ ] PDF in `/docs/p2`, tag `p2` pushed, the same PDF uploaded to Canvas by John only
- [ ] All six signed section 12
- [ ] Every AI tool use declared in 10.5, including commits with an AI co-author line
