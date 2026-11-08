# 7 Design Rationale

## 7.1 Architecture decision records

Each record names the drivers that forced the decision, the options the team actually weighed, what was chosen and what that choice costs.

### ADR-02 Self-hosted Moodle as the LMS

| Field | Record |
|---|---|
| Status | Accepted |
| Date and owner | Decided Nov 7, 2026 by John Bramlet (prototype commit `b5c18f7`); recorded by Daniel Habib |
| Context (drivers) | The agent must read a student's courses, assignments and submission status through an LMS API (FR-02, FR-04) with that student's own access (QR-03), and the team must be able to run it within the course's resources (CON-02). P1 left the platform open (Q1) and rated setting up open-source Canvas as a high-likelihood, high-impact risk (R1). |
| Options considered | (a) Canvas Lite, the free hosted Canvas: blocks API tokens for every account, so the agent could not connect. (b) Self-hosted open-source Canvas, P1's plan: the setup risk R1. (c) Google Classroom: needs a Google Cloud OAuth app before any API call. (d) Self-hosted Moodle 5.3 with PostgreSQL in Docker, read through Moodle's web-service API with the student's own token. |
| Decision | (d) Self-hosted Moodle 5.3. CON-01 now names Moodle, which answers Q1. |
| Consequences | Favors feasibility and schedule: the API works today, costs nothing, and any member can run Moodle on a laptop. Cost: it is not the LMS UT Dallas students use, so the agent cannot reach their real courses and all course content is our own sample data (R3). The team hosts, seeds and upgrades Moodle itself. The LMS adapter (`lms.py`) is Moodle-specific, so supporting Canvas later means writing a second adapter behind the same seven tool methods. |
| Evidence | Working prototype against Moodle: commits `b5c18f7` (agent and Moodle adapter), `f019be3` (Moodle install fix), `c5ee6e5` (sample course seed). Canvas Lite token block: `ONBOARDING.md`, section 1. |
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
