# 2 Overall Description

## 2.2 Stakeholders and evidence

Primary stakeholder: a student using Moodle to track coursework, understand course materials, and practice concepts. Other stakeholders include instructors whose course policies must be respected and administrators responsible for LMS access and data protection.

The prototype supports asking about courses, assignments, syllabus, pages, modules and announcements. These are prototype capabilities, not proof that students requested them. P1 feedback identified stakeholder needs as assumptions. To address that, circulate the five-question survey below and report the actual sample size, counts and response percentages. Do not characterize an uncollected survey as evidence.

Survey (anonymous, voluntary): (1) How often do you miss or nearly miss LMS deadlines? Never/Rarely/Sometimes/Often. (2) Which LMS tasks are hardest? Select all: find deadlines, find assignment instructions, understand syllabus policies, review notes, practice concepts, other. (3) How useful would an AI assistant embedded in the LMS be? 1–5. (4) Which concern matters most? Accuracy, privacy, speed, academic integrity, accessibility, other. (5) Would you use a read-only study assistant that does not complete graded work? Yes/Maybe/No. Do not collect names or student IDs.

Evidence status: no survey responses or aggregate results have been supplied in this contribution. The stakeholder needs above remain assumptions supported by the project's intended scope, not validated student findings. No sample size, response counts, percentages or usefulness score is claimed. If the survey is completed, publish anonymized aggregate results and the collection method before using it as stakeholder evidence. A convenience sample of classmates would be exploratory, not representative of all students. The P1 stakeholder-evidence issue remains open.

## 2.4 Feasibility update

Technical feasibility — implementation evidence exists; independent runtime validation and production readiness remain unverified. [Prototype commit b5c18f7](https://github.com/azghier1/Ai-Agent/commit/b5c18f7) adds the agent and Moodle adapter; [commit 347886c](https://github.com/azghier1/Ai-Agent/commit/347886c) adds the web chat and Moodle bubble. The [Docker configuration](https://github.com/azghier1/Ai-Agent/blob/20f021ff8db8a4827aeb2d1a4ac3ee82ff94abbf/docker-compose.yml) specifies Moodle 5.3 and PostgreSQL. The adapter implements course and assignment retrieval and the agent exposes seven read-only tools. These are code and configuration evidence; this contribution does not provide an independently reproduced end-to-end demo log.

Integration feasibility — conditional. The team's [onboarding record](https://github.com/azghier1/Ai-Agent/blob/20f021ff8db8a4827aeb2d1a4ac3ee82ff94abbf/ONBOARDING.md#1-where-the-project-is) reports that its Canvas Lite environment did not provide the needed token access, motivating the move to self-hosted Moodle. This records the team's environment-specific finding, not a claim about every Canvas deployment. The prototype relies on one configured student's token; it does not provide identity isolation for multiple real students. LTI 1.3 and a way to obtain each student's authorized Moodle access are planned, not implemented.

Performance feasibility — open. QR-01's target (95% of responses within 5 seconds under 20 concurrent users) is not verified by this contribution. John's Section 8 S-01 experiment is the designated evidence source. Its actual results must determine the verdict; no timing or pass/fail outcome is claimed here.

Privacy/security feasibility — conditional. Student question/context is sent to the external Anthropic Claude API over HTTPS. The current shared-token approach can expose one test student's data to anyone reaching the chat server. Production deployment requires per-user authentication, authorization and privacy review; the current prototype is for test data only.

Operational/economic feasibility — conditional. Moodle and the chat server require hosting and maintenance, and Claude API usage incurs cost. Document actual usage costs and deployment assumptions before a production verdict.

Verdict: the repository provides an implemented prototype and documented setup path using synthetic/test data. This supports a limited technical feasibility assessment, while stakeholder validation, independently reproduced integration, production identity/privacy, performance and operating cost remain unresolved. Production deployment feasibility is not yet established.

Additional implementation evidence: [student-token Moodle REST adapter and mock data interface](https://github.com/azghier1/Ai-Agent/blob/20f021ff8db8a4827aeb2d1a4ac3ee82ff94abbf/lms.py), [chat endpoint and shared-token/session limits](https://github.com/azghier1/Ai-Agent/blob/20f021ff8db8a4827aeb2d1a4ac3ee82ff94abbf/server.py), and [agent prompt, model loop and read-only tools](https://github.com/azghier1/Ai-Agent/blob/20f021ff8db8a4827aeb2d1a4ac3ee82ff94abbf/agent.py). Missing evidence is explicit: survey results, a reproducible live integration record, S-01 measurements and usage-cost records have not been supplied here. Section 9 maps these limitations to requirements and follow-up work.
