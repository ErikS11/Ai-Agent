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
