# 6. High-Level Design

**Author:** Ahmad Zghier, System Architect  
**System:** Group 1 LMS AI Study Assistant  
**Status:** P2 design baseline; proposed quality targets are not verified performance results. Cross-section checks require teammates' final sections.

**Implementation evidence:** [`ONBOARDING.md`](../../../ONBOARDING.md), [`docs/p2/WORK_PLAN.md`](../WORK_PLAN.md), and repository sources [`server.py`](../../../server.py), [`agent.py`](../../../agent.py), [`lms.py`](../../../lms.py), [`web/embed.js`](../../../web/embed.js), [`web/chat.html`](../../../web/chat.html), and [`docker-compose.yml`](../../../docker-compose.yml).

## 6.1 Quality Attribute Scenarios

| ID / attribute | Source and stimulus | Environment and affected artifact | Expected response | Measurable response / verification |
|---|---|---|---|---|
| **QAS-01 Performance (QR-01)** | 20 students concurrently submit ordinary course questions | Running Moodle-backed prototype; browser chat, FastAPI server, agent, LMS adapter and Claude API | The system retrieves permitted course context and returns an answer without blocking unrelated requests | **At least 95 of 100 requests finish within 5.0 seconds**, measured from HTTP request submission to complete HTTP response, with 20 concurrent requests per batch. Record p50, p95, errors, model and LMS configuration. **Target, not yet demonstrated;** Zaid's S-01 spike provides evidence. |
| **QAS-02 Access control (QR-03)** | A student attempts to access another student's assignment/grade or invokes the chat without a valid student session | Authenticated production-style integration, including the chat API and Moodle web services | Reject unauthenticated requests; retrieve only data authorized for the requesting student; do not reveal another student's data | **100% of 20 negative authorization test cases** return no protected information; invalid or missing credentials result in HTTP 401/403 (or equivalent safe rejection). **Not satisfied by current single-token prototype;** per-student LTI 1.3 identity is planned for P3. |
| **QAS-03 Failure handling (FR-07)** | Moodle is unavailable or returns a failed API response while a student asks about an assignment | Chat UI, FastAPI server and LMS adapter during an LMS outage | Display an understandable error without fabricating assignment details or exposing secrets | **At least 19 of 20 injected LMS-failure cases** produce a visible, non-sensitive error response within **10 seconds**; **0 of 20** present fabricated Moodle data as verified fact. Target for P3 testing, not a measured result. |

## 6.2 Architectural Style and Alternatives

**Selected: layered client-server architecture with an external AI service.** The presentation layer is the Moodle-embedded chat interface (`web/embed.js`, `web/chat.html`). The application/API layer is FastAPI (`server.py`) and the agent orchestration (`agent.py`). The LMS integration layer is `lms.py`, which translates the seven read-only agent tools into Moodle REST web-service requests. Moodle 5.3 and PostgreSQL own authoritative course records; Anthropic Claude is a separate, externally hosted inference service. This is a logical layering decision, not a claim that each layer has its own physical server.

**Why it fits:** (1) the chat interface can change without changing Moodle integration; (2) the adapter allows `MockLMS` for offline tests; (3) Moodle remains the source of truth; (4) read-only LMS tools limit accidental modification; and (5) the external API trust boundary is explicit. **ADR-01** in Section 7 should document this exact choice.

**Rejected alternative A: monolithic Moodle plugin.** Embedding the entire AI workflow into Moodle would reduce the number of separate services but couple agent upgrades, external AI credentials, testing, and deployment to Moodle internals. It would be harder to run the existing terminal/mock implementation independently.

**Rejected alternative B: event-driven microservices.** Separate services and queues for chat, retrieval, tool execution and inference could improve isolation at scale, but would add deployment, observability, message-ordering and debugging overhead to a small course prototype. The request/response interaction and limited team size do not justify that complexity yet.

**Consequences:** External Claude calls create latency, availability, cost and student-data-disclosure risks. The present local HTTP setup is development-only; production requires TLS, student-specific identity, careful data minimization, and server-side secret handling.

## 6.3 Component View

See editable **`docs/p2/diagrams/component-view.puml`** and exported **`component-view.png`**. The UML component view identifies the Moodle page, embedded launcher and chat panel, FastAPI chat endpoint, agent orchestrator, read-only tools, LMS adapter, Moodle web services, PostgreSQL and Claude API. Solid arrows represent synchronous calls, not database ownership. The browser does **not** connect directly to PostgreSQL or Anthropic.

**Typical flow:** (1) student opens Moodle and the embedded chat; (2) chat posts a question to `/api/chat`; (3) the agent sends the question and tool definitions to Claude; (4) if Claude requests a tool, the agent invokes `lms.py`; (5) the adapter calls Moodle REST using the configured student token; (6) Moodle reads the relevant records from PostgreSQL; (7) tool results return to the agent and Claude generates the response; (8) FastAPI returns the response to the chat. Claude may make multiple tool calls, so one chat turn can involve multiple external requests.

**Traceability:** The chat UI and API support **UC-01 Ask Course-Related Questions**, the agent and adapter support **UC-02 Organize Assignments** and **UC-03 View Upcoming Deadlines**; the tutor prompt supports the planned **UC-04 Generate Practice Questions**; read-only tools support data-integrity constraints; authorization boundary supports QAS-02; error-handling path supports QAS-03; API/orchestration path is measured by QAS-01. The prototype currently lacks answer source citations, a dedicated seven-day cross-course aggregation endpoint, and verified practice-question behavior.

## 6.4 Deployment View and Trust Boundaries

See editable **`docs/p2/diagrams/deployment-view.puml`** and exported **`deployment-view.png`**.

| Node / boundary | Deployed elements | Communication and data |
|---|---|---|
| Student device/browser | Moodle web page, injected `embed.js`, iframe chat page | Browser loads Moodle over local HTTP port 8080 and chat/API over local HTTP port 8000 in the prototype. Production must use HTTPS and appropriate origin controls. |
| Local development host | Python FastAPI `server.py`, `agent.py`, `lms.py`; in-memory `sessions` and per-session locks | `/api/chat` invokes orchestration; LMS adapter calls Moodle REST. The server retains chat messages in RAM while running (up to 200 sessions, with eviction); it does **not** persist a conversation database. Current configuration uses one test student's token, **not** real per-user authentication. |
| Docker: Moodle container | Moodle 5.3, REST web services | Authoritative LMS authorization and course operations. |
| Docker: PostgreSQL container | Moodle database | Stores course, user, assignment, grade, page and announcement data; only Moodle should query it. |
| External Anthropic infrastructure | Claude model/API | Agent sends student prompts and selected course/tool context over HTTPS. **Data leaves the team's host and control at this boundary.** API credentials must remain server-side. |

**Security/privacy implications:** Sending identifiable course or grade information to Anthropic may involve education records; the team must evaluate institutional policy, FERPA applicability, vendor terms, retention, consent and minimization before using real student data. The chat API currently has **no per-student authentication check**, and a browser-supplied session ID refers to server-side chat history, not a verified student identity. All chat requests use the same configured Moodle token. Therefore the prototype is suitable for synthetic/test data, not proof of production FERPA compliance. LTI 1.3 student identity and authorization checks are planned for P3. No passwords, tokens or API keys belong in diagrams, repository commits or client JavaScript.

## 6.5 Analysis-to-Component Mapping

This mapping reflects the currently documented entities and must be reconciled against Omor's final Section 5.1 domain model before the P2 PDF is assembled. **Ownership** means the authoritative record system, not necessarily the component that displays it.

| Domain concept | Authoritative owner | Access / presentation component | Notes |
|---|---|---|---|
| Student | Moodle user/account model and PostgreSQL | Moodle REST → `MoodleLMS` → agent/chat | Single test token today; per-student identity is a P3 gap. |
| Course / enrollment | Moodle course/enrollment models | `MoodleLMS` course-list tool; agent/chat | Access restricted to the authenticated student's courses in intended design. |
| Assignment / due date / submission status | Moodle assignment and submission records | Assignment-list and assignment-detail tools | Seven-day cross-course filtering is planned, not implemented as a dedicated tool. |
| Grade | Moodle gradebook | Course/assignment retrieval tools | Sensitive student data; never persisted by the agent as a second source of truth. |
| Announcement | Moodle course announcements/forum data | Announcement-list tool | Read-only retrieval. |
| Course module / page / syllabus | Moodle course content | Module, page and syllabus tools | The assistant summarizes retrieved content. |
| Student question / generated answer / chat session | Agent-server process memory (`server.py` `sessions` dictionary), not persistent storage | `web/chat.html`, `server.py`, `agent.py`, Claude | Chat messages are retained in server RAM until reset, eviction or restart. No durable conversation database exists in the documented prototype. |
| AI tool invocation | Agent orchestrator (`agent.py`) | `lms.py` executes the selected read-only Moodle operation | Tool definitions belong to the agent; Moodle owns returned academic records. |

## 6.6 Design Principles

1. **Separation of concerns:** `web/chat.html` and `web/embed.js` handle interaction; `server.py` exposes HTTP endpoints; `agent.py` orchestrates model/tool calls; `lms.py` handles Moodle-specific access. This makes the components independently understandable and testable.
2. **Dependency inversion at the LMS boundary:** `MoodleLMS` and `MockLMS` provide real and offline data access paths. The agent does not need to embed raw Moodle REST calls in the chat UI.
3. **Least privilege and read-only operation:** The seven LMS tools retrieve course data but do not submit assignments, change grades or edit Moodle. The intended production design scopes access to the requesting student; current shared-token behavior is a documented limitation.
4. **Single source of truth:** Moodle/PostgreSQL own academic records. The agent requests current information instead of maintaining a separate writable copy of grades and assignments.
5. **Explicit trust boundaries:** External Claude requests are separated from Moodle's internal database and the browser. Sensitive tokens stay server-side; outbound student data requires policy review and minimization.
6. **Testability and measurable design:** `MockLMS` supports deterministic offline checks; QAS-01 defines a repeatable concurrent load experiment; QAS-02 and QAS-03 specify negative authorization and outage tests. Passing results are not claimed until observed.
7. **Evolutionary design:** Keep the simple layered system for P2, then add LTI 1.3 identity, citations, accessible chat, cross-course deadlines, and latency improvements in P3 without rewriting Moodle.

**Outstanding cross-section checks before final submission:** Erik's PR #4 currently uses UC-01 Ask Course-Related Questions, UC-02 Organize Assignments, UC-03 View Upcoming Deadlines, and UC-04 Generate Practice Questions; confirm those stay unchanged after merging; align the ownership rows with Omor's final domain diagram; ensure Daniel's pending ADR-01 selects the same layered client-server style (Daniel's PR #2 currently starts at ADR-02); replace QAS-01's unverified status with a reference to Zaid's actual spike results when available; and ensure the team AI-use table declares ChatGPT assistance for this section.

**Version check:** This section describes the P2 prototype, not features promised for P3. Targets in QAS-01–03 are requirements/test plans, not passing test outcomes.
