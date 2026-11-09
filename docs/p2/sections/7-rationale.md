# 7 Design Rationale

## 7.1 Architecture decision records

Each record names the drivers that forced the decision, the options the team actually weighed, what was chosen and what that choice costs. ADR-01 records the architectural style chosen in section 6.2.

### ADR-01 Layered client-server architecture with an external AI service

| Field | Record |
|---|---|
| Status | Accepted |
| Date and owner | Decided Nov 8, 2026 by Ahmad Zghier (section 6.2, commit `9aec1ea`); recorded by Daniel Habib |
| Context (drivers) | At least 95 of 100 requests must finish within 5.0 seconds with 20 concurrent requests (QAS-01), 100% of 20 negative authorization tests must return no protected information (QAS-02), and at least 19 of 20 injected LMS failures must produce a visible, non-sensitive error within 10 seconds (QAS-03). The system must work with Moodle (CON-01) within the team's resources and one term (CON-02). |
| Options considered | (a) Layered client-server: the chat panel and launcher in the student's browser, an agent server (chat endpoint, agent orchestrator, read-only tools), an LMS adapter in front of Moodle, and Claude as an external service. (b) Monolithic Moodle plugin: the whole AI workflow built into Moodle. (c) Event-driven microservices: separate services and queues for chat, retrieval, tool execution and inference. |
| Decision | (a) Layered client-server with an external AI service. |
| Consequences | Favors modifiability and testability: the chat interface, agent and LMS adapter change independently, `MockLMS` stands in for Moodle in offline tests, Moodle stays the single source of truth, and student data leaves for Claude along one explicit path (QAS-02). An LMS failure surfaces in one layer, the adapter, where it can become a clear message (QAS-03). Cost: every question passes through each layer synchronously, plus one or more round trips to Claude, so delays add up (QAS-01, measured by S-01). The agent server is a single process that keeps chat sessions in memory, so it cannot scale out and loses chat history on restart. Compared with (b), it is one more service to run and secure beside Moodle; compared with (c), it gives up isolation at large scale. |
| Evidence | The prototype already follows these layers: `web/` (presentation), `server.py` and `agent.py` (application), `lms.py` (LMS integration), commits `b5c18f7` and `347886c`. S-01 (section 8) measures the latency cost against QAS-01. |
| Related | ADR-03, ADR-04, QAS-01, QAS-02, QAS-03, S-01 |

### ADR-02 Self-hosted Moodle as the LMS

| Field | Record |
|---|---|
| Status | Accepted |
| Date and owner | Decided Nov 7, 2026 by John Bramlet (prototype commit `b5c18f7`); recorded by Daniel Habib |
| Context (drivers) | The agent must read a student's courses, assignments and submission status through an LMS API (FR-02, FR-04) with that student's own access (QR-03), and the team must be able to run it within the course's resources (CON-02). P1 planned on Canvas but left the final platform open (Q1). |
| Options considered | (a) Canvas, free version: does not allow third-party services such as our agent to connect, so the agent could not read any course data. (b) Google Classroom: needs a Google Cloud OAuth app before any API call. (c) Self-hosted Moodle 5.3 with PostgreSQL in Docker, read through Moodle's web-service API with the student's own token. |
| Decision | (c) Self-hosted Moodle 5.3. CON-01 now names Moodle, which answers Q1. |
| Consequences | Favors feasibility and schedule: the API works today, costs nothing, and any member can run Moodle on a laptop. Cost: it is not the LMS UT Dallas students use, so the agent cannot reach their real courses and all course content is our own sample data (R3). The team hosts, seeds and upgrades Moodle itself. The LMS adapter (`lms.py`) is Moodle-specific, so supporting Canvas later means writing a second adapter behind the same seven tool methods. |
| Evidence | Working prototype against Moodle: commits `b5c18f7` (agent and Moodle adapter), `f019be3` (Moodle install fix), `c5ee6e5` (sample course seed). Canvas free-version block: `ONBOARDING.md`, section 1. |
| Related | ADR-04, ADR-05, CON-01, Q1, R1, R3 |

### ADR-03 Fetch course data on demand through read-only tools

| Field | Record |
|---|---|
| Status | Accepted |
| Date and owner | Decided Nov 7, 2026 by John Bramlet (prototype commit `b5c18f7`); recorded by Daniel Habib |
| Context (drivers) | Answers must come only from the student's own enrolled courses (FR-02, FR-03) and reflect live assignment status (FR-04 to FR-06), at least 95% of answers must arrive within 5 seconds with 20 concurrent users (QR-01), and accuracy must reach 95% on the evaluation set (QR-04). LLM cost is a known risk (R4). |
| Options considered | (a) Tool calling on demand: the model chooses among seven read-only tools (courses, assignments, assignment instructions, syllabus, modules, pages, announcements) and the agent reads Moodle live for each question. (b) Preload: fetch all of the student's course content and send it with every question. (c) Search index (RAG): copy course content into an index ahead of time and send the best-matching passages with each question. |
| Decision | (a) Tool calling on demand. Every tool only reads; nothing writes to the LMS. |
| Consequences | Favors freshness and least privilege: due dates, submission status and grades are read at the moment of asking, each read uses the student's own access, and no copy of student records is stored on our side. Only what a question needs is sent to the model provider, where preloading would send the whole course each time. Cost: one question can take several model turns, each waiting on the model and on Moodle (listing assignments makes one Moodle call per assignment), which puts QR-01 at risk and multiplies API cost per question (R4). Answer quality depends on the model picking the right tools, and with no full-text search a fact on an unvisited page can be missed (R2). |
| Evidence | Agent loop in `agent.py` and per-assignment status calls in `lms.py` (commit `b5c18f7`). Spike S-01 (section 8) measures this design's response time against QR-01. |
| Related | S-01, QR-01, QR-04, FR-03, R2, R4 |

### ADR-04 Reach students through a chat bubble inside Moodle

| Field | Record |
|---|---|
| Status | Accepted |
| Date and owner | Decided Nov 7, 2026 by John Bramlet (commit `347886c`); recorded by Daniel Habib |
| Context (drivers) | Students already know their LMS but cannot be assumed to know our agent (section 2.3), and they need a comparable experience across devices (section 2.4). First-time students must find their assignments quickly (QR-02). |
| Options considered | (a) Terminal app: kept for testing, unusable for most students. (b) Standalone web page: a separate site students would have to find and open. (c) Chat bubble: a script added once through Moodle's "Additional HTML" setting puts a button on every signed-in Moodle page that opens our chat page in a panel. (d) Moodle plugin written in PHP and installed into Moodle. |
| Decision | (c) Chat bubble inside Moodle. The standalone page stays available at the agent server's root as a fallback. |
| Consequences | Favors usability: the assistant sits where students already are, with no new site to find, and the panel fits phone-width screens. The agent stays a separate service that can change without reinstalling anything in Moodle, which a plugin (d) would require. Cost: a Moodle administrator must allow our script on every page, which a university's LMS team would have to approve. The panel is served from our server, not Moodle, so it does not inherit the student's Moodle sign-in (see ADR-05) and does not know which course page the student is on. Our server must be reachable from every student's browser. |
| Evidence | Chat page and bubble: commit `347886c` (`web/chat.html`, `web/embed.js`, `server.py`); setup in `README.md`, section 4. |
| Related | ADR-02, ADR-05, QR-02 |

### ADR-05 Read the LMS only with the student's own credential

| Field | Record |
|---|---|
| Status | Accepted: a configured test token for the prototype, LTI 1.3 sign-in for P3 |
| Date and owner | Decided Nov 7, 2026 by John Bramlet (commit `b5c18f7`); recorded by Daniel Habib |
| Context (drivers) | Unauthorized access to course material must be denied 100% of the time (QR-03), the agent may read only the student's enrolled courses (FR-02), student records fall under FERPA, and OIT needs the agent kept inside the access a student already has (section 2.2, Q3). P1 also named campus sign-in as a constraint (section 2.4). |
| Options considered | (a) One test student's token, set in the server's configuration. (b) Each student pastes their own Moodle security key into the chat. (c) LTI 1.3: Moodle launches the agent and tells it which student is signed in. |
| Decision | Every LMS read uses the signed-in student's own Moodle token, so Moodle itself decides what the agent may see. (a) for the P2 prototype only, (c) as the P3 sign-in. (b) was rejected because it asks every student to find and handle a credential. |
| Consequences | Favors security and privacy: the agent never holds more access than the student, so a bug or a manipulated prompt cannot reveal another student's grades, because Moodle refuses the request. Cost: the prototype cannot demonstrate QR-03 across students, since every chat uses one test student's token and the chat API does not yet check who is calling. LTI 1.3 identifies the student but does not by itself give the agent that student's Moodle token, so P3 must add a way to obtain one; falling back to one privileged account would move QR-03 enforcement into the agent and supersede this record. Campus sign-in (section 2.4) is met only through the student's Moodle sign-in. |
| Evidence | `lms.py` sends every Moodle call with the student's token (commit `b5c18f7`); prototype limits in `README.md`, section 4. Per-student sign-in: none yet. |
| Related | ADR-02, ADR-04, QR-03, FR-02, Q3 |

## 7.2 Trade-off summary

| Quality favored | Architectural move | Cost accepted | Recorded in |
|---|---|---|---|
| Modifiability, testability | Layered client-server with Claude as an external service | Delays add up across layers (QAS-01); one in-memory agent server that cannot scale out | ADR-01 |
| Feasibility, schedule | Self-host Moodle 5.3 instead of Canvas | Not the LMS students use; sample data only; the team hosts it; a Moodle-specific adapter | ADR-02 |
| Data freshness, least privilege | Read course data live through read-only tools the model calls | Several model turns per question: response time (QR-01, measured by S-01) and API cost (R4) | ADR-03 |
| Usability | Chat bubble on every Moodle page | An admin-approved site-wide script; no inherited sign-in or course context; a server every student must reach | ADR-04 |
| Security, privacy | Every LMS read uses the student's own token | Per-student sign-in still to build; the prototype runs on one test token | ADR-05 |
