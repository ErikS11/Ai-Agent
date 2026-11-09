Section 2 — Overall Description (Zaid draft)

2.2 Stakeholders and evidence

Primary stakeholder: a student using Moodle to track coursework, understand course materials, and practice concepts. Other stakeholders include instructors whose course policies must be respected and administrators responsible for LMS access and data protection.

The prototype supports asking about courses, assignments, syllabus, pages, modules and announcements. These are prototype capabilities, not proof that students requested them. P1 feedback identified stakeholder needs as assumptions. To address that, circulate the five-question survey below and report the actual sample size, counts and response percentages. Do not characterize an uncollected survey as evidence.

Survey (anonymous, voluntary): (1) How often do you miss or nearly miss LMS deadlines? Never/Rarely/Sometimes/Often. (2) Which LMS tasks are hardest? Select all: find deadlines, find assignment instructions, understand syllabus policies, review notes, practice concepts, other. (3) How useful would an AI assistant embedded in the LMS be? 1–5. (4) Which concern matters most? Accuracy, privacy, speed, academic integrity, accessibility, other. (5) Would you use a read-only study assistant that does not complete graded work? Yes/Maybe/No. Do not collect names or student IDs.

Results placeholder — replace only with actual data: Responses n = [NOT COLLECTED]. Deadline difficulty: [COUNTS]. Top tasks: [COUNTS]. Mean usefulness: [NOT MEASURED]. Top concern: [COUNTS]. Would use: [COUNTS]. Sampling limitation: convenience sample of classmates; results are exploratory, not representative of all students.

2.4 Feasibility update

Technical feasibility — prototype demonstrated, production readiness unverified. The repository documents a self-hosted Moodle 5.3 instance in Docker with PostgreSQL, an LMS adapter using Moodle web-service calls, an agent with seven read-only tools, and a web/chat-bubble interface. The documented workflow supports course and assignment retrieval, but a repeatable demo log or test evidence should be linked before claiming end-to-end validation.

Integration feasibility — conditional. Canvas Lite did not provide the required API token access in the team's evaluation, so the team switched to self-hosted Moodle. The prototype relies on a configured single student's token; this is not suitable for multiple real student accounts. LTI 1.3 is planned, not implemented.

Performance feasibility — open. QR-01's target (95% of responses within 5 seconds under 20 concurrent users) is not verified. Section 8's S-01 spike will supply evidence; do not state pass/fail until measured.

Privacy/security feasibility — conditional. Student question/context is sent to the external Anthropic Claude API over HTTPS. The current shared-token approach can expose one test student's data to anyone reaching the chat server. Production deployment requires per-user authentication, authorization and privacy review; the current prototype is for test data only.

Operational/economic feasibility — conditional. Moodle and the chat server require hosting and maintenance, and Claude API usage incurs cost. Document actual usage costs and deployment assumptions before a production verdict.

Verdict: feasible as a limited prototype using synthetic/test data; not yet demonstrated feasible for production deployment until identity, privacy, performance and operational risks are addressed.

Evidence to insert: GitHub links to relevant commits/README; actual survey summary; S-01 measurements; course/demo screenshots if verified.
