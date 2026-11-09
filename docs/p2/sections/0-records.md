# 0 Revision History, Contribution Record and Changes Since P1

| Version | Date | Author | Summary of change |
|---|---|---|---|
| 0.1 | Oct 18, 2026 | John Bramlet | Set up the shared document from the course template; completed sections 0 and 1 of P1 |
| 0.2 | Oct 18, 2026 | Zaid Abusamra, Omor Igiehon | Completed section 2: context diagram, stakeholders, user characteristics, constraints, assumptions and feasibility |
| 0.3 | Oct 18, 2026 | Erik Sandoval | Completed section 3: FR-01 to FR-08, QR-01 to QR-04, CON-01 and CON-02, use-case diagram, UC-01 and UC-02, traceability matrix |
| 0.4 | Oct 18, 2026 | Daniel Habib, Ahmad Zghier | Completed sections 4 and 5 of P1: team roles, plan to P2, risks and open questions |
| 0.5 | Oct 18, 2026 | John Bramlet | P1 baseline as submitted (issued as "1.0" at P1; renumbered under CH-09 so that the P2 baseline is 1.0) |
| 0.6 | Nov 7, 2026 | John Bramlet | Working prototype committed: agent, Moodle adapter, Moodle deployment, sample course, chat bubble; team onboarding guide and P2 work plan |
| 0.7 | Nov 8, 2026 | All members | Sections 2 to 9 added or updated through pull requests (see 0.1) |
| 1.0 | Nov 8, 2026 | John Bramlet | P2 baseline: analysis and high-level design added; sections 0, 1 and 10 to 12 updated |

## 0.1 Individual contribution record (P2)

| Team member | Sections and artifacts this person produced for P2 | Evidence in the repository (commit hashes, PR numbers) | Reviews given (PR numbers) |
|---|---|---|---|
| John Bramlet | Sections 0, 1 (update), 10, 11 and 12; final PDF assembly and tag `p2`. Before P2 drafting: the working prototype the design describes (agent, Moodle LMS adapter, Moodle deployment and sample-course seed, chat page and Moodle chat bubble), the team onboarding guide and the P2 work plan | Prototype on `main`: `b5c18f7`, `f019be3`, `c5ee6e5`, `347886c`. PR #1 (onboarding guide, work plan): `9b3bad1`, `4db0b68`, `124579b`, `b908084`. Sections 0, 1, 10 to 12: PR #6 | PR #4 (Erik) |
| Erik Sandoval | Section 3 update (QR-02 reworded, CON-01 changed to Moodle, use-case IDs reconciled to UC-01 to UC-04, use-case diagram) and section 4 (use cases selected, expanded, self-reviewed) | PR #4: `07e984f`, `d8b9049` | |
| Omor Igiehon | No P2 work in the repository at the time of assembly | None | None |
| Daniel Habib | Section 5.2 for UC-02 (non-trivial steps, scenario table, analysis sequence diagram and its source) and section 7 (ADR-01 to ADR-05, trade-off summary) | PR #2: `5152e68`, `957ab26`, `874853c`, `d1dc743`, `ddaeb1b`, `7a09149`, `02838bb`, `0209b82`. PR #3: `dce6a7d`, `7c18fb6`, `13fb907`, `00031c3`, `19f1888`, `aa28138` | PR #5 (Ahmad): changes requested, then approved |
| Ahmad Zghier | Section 6 (QAS-01 to QAS-03, style and alternatives, component view, deployment view, analysis-to-component mapping, design principles) with diagram sources | PR #5 (merged as `4d85643`): `9aec1ea`, `e6b95e0`, `6d5b491`, `35dbf54`, `bc798e2`, `64a375a`, `949ef0c`, `7ce4bbb`, `575ec50`, `56c5ea0` | |
| Zaid Abusamra | Section 2 update (survey instrument, feasibility verdicts tied to evidence) | Branch `docs/zaid-p2-sections`: `20f021f` | |

## 0.2 Changes since the P1 baseline

| Change ID | What changed (IDs affected) | Why (P1 feedback, new finding, spike result) | Knock-on effect | Agreed on |
|---|---|---|---|---|
| CH-01 | Repository in use: every P2 section reaches `main` through a reviewed pull request; 0.1 cites commit hashes and PR numbers | P1 feedback (C4, C5): the repository had no commits, so conventions and contributions could not be verified | 10.4 describes the layout and the PR rule; the contribution record is checkable | Nov 8 |
| CH-02 | LMS changed from Canvas to self-hosted Moodle 5.3 (CON-01 reworded; 1.1 and 1.3 updated; Q1 closed) | Canvas Lite, the free hosted Canvas, blocks personal API tokens for every account, so the agent could not connect. Moodle's web-service API works from a self-hosted instance | ADR-02; R1 closed; sample data loaded into Moodle (R3); the LMS adapter is Moodle-specific | Nov 7 |
| CH-03 | Feasibility verdicts in 2.6 tied to evidence | P1 feedback (C1): verdicts were conditional with no checkable evidence. The prototype now makes working calls against a self-hosted LMS API (commits `b5c18f7`, `c5ee6e5`) | Technical feasibility rests on the prototype; performance feasibility waits on spike S-01 (section 8) | Nov 8 |
| CH-04 | Stakeholder needs in 2.2: a five-question student survey replaces assumption as the method | P1 feedback (C1): needs were stated as assumptions | Survey results are tracked in Q4 until reported | Nov 8 |
| CH-05 | Use-case IDs reconciled to UC-01 to UC-04 (3.4); the P1 matrix's UC-05 reference corrected to UC-04 | P1 feedback (C3): matrix referred to UC-03 and UC-05 while the diagram showed UC-01 to UC-04 | Section 4 and the matrix in 9.1 use the same four IDs | Nov 8 |
| CH-06 | QR-02 reworded with task, population, threshold, time limit and sample size | P1 feedback (C3): QR-02 could not be tested | QR-02 is now verifiable by a 10-student usability test | Nov 8 |
| CH-07 | Contribution record cites real repository evidence | P1 feedback: the contribution table said repository links were "to be added" | 0.1 | Nov 8 |
| CH-08 | Use-case detail moved from 3.4 to section 4; the P1 matrix in 3.5 replaced by a pointer to 9.1 | P2 template structure | No content lost; IDs preserved | Nov 8 |
| CH-09 | Document version numbering: P1 baseline renumbered 0.5 | P1 was issued as "1.0"; the P2 baseline must be 1.0 | Revision history above | Nov 8 |
| CH-10 | Campus sign-in constraint (2.4) met for now only through the student's own Moodle sign-in and token; per-student sign-in through LTI 1.3 planned for P3 | Prototype finding: the chat service runs on one configured test-student token | ADR-05; QAS-02 not yet demonstrable; R7 | Nov 8 |
| CH-11 | Plan, risks and open questions updated (10.2, 10.3, 11): R1 closed, R6 to R8 added, Q1 to Q3 closed, Q4 to Q6 added | Analysis and design findings, platform change | Sections 10 and 11 | Nov 8 |
