
# 4 Use-Case Analysis

This section expands three student-facing use cases from Section 3.4. The scenarios describe required user-visible behavior rather than internal implementation. UC-01 and UC-02 were introduced in P1; UC-04 covers practice-question generation.

## 4.1 Use Cases Selected for Analysis

| Use case | Name | Why it was selected | Non-trivial steps |
|---|---|---|---|
| UC-01 | Ask Course-Related Questions | This is the primary purpose of the assistant. It must provide grounded answers, protect course access, and handle unavailable information. | Steps 2, 4, 6 |
| UC-02 | Organize Assignments | Students need to understand their assignments, deadlines, and submission statuses. Missing dates and unavailable records introduce important alternatives. | Steps 2, 4 |
| UC-04 | Generate Practice Questions | This supports the project's study-assistance goal and requires the system to generate relevant questions without completing graded work. | Steps 2, 4 |

These use cases were selected for their importance to students, requirement coverage, and the risks associated with missing or inaccessible course information.

## 4.2 Expanded Use Cases

### UC-01 — Ask Course-Related Questions

| Field | Description |
|---|---|
| Primary actor | Student |
| Supporting actors and external systems | Learning Management System (Moodle) |
| TUCBW | The student wants an answer to a question about an enrolled course. |
| TUCEW | The student receives an answer with its supporting course reference, or an understandable explanation of why the request could not be completed. |
| Preconditions | The student is authenticated and has access to at least one enrolled course. |
| Postconditions | On success, the student has received a course-grounded answer and a supporting source reference. On failure, the student has been informed why an answer cannot be provided. |
| Traces to requirements | FR-01, FR-02, FR-03, FR-07, QR-03, QR-04, CON-01 |

#### Main Success Scenario

| Actor input/action | System response |
|---|---|
| — | (0) The system presents the student's available courses and indicates that course-related questions can be asked. |
| (1) The student selects a course. | (2) The system confirms the selected course and invites the student to ask a question. |
| (3) The student submits a question about the course material. | (4) The system presents an answer supported by accessible course information and identifies the source material used. |
| (5) The student asks to examine the supporting material. | (6) The system identifies the relevant course page, assignment, or other source and confirms that the supporting material has been located. |

#### Alternate and Exception Flows

| Flow | At step | Condition | What happens | Ends or rejoins at |
|---|---|---|---|---|
| A1 | 4 | The course material does not contain sufficient information to answer the question. | The system explains that the available material does not support an answer and does not invent one. | Ends with an insufficient-information notification. |
| A2 | 4 | The requested course information cannot be retrieved. | The system informs the student that the information is temporarily unavailable and that the request was not completed. | Ends with a failure notification. |
| A3 | 2 | The selected course is not accessible to the student. | The system denies access to that course, explains the restriction, and offers the student's available courses. | Rejoins at step 1. |
| A4 | 6 | The supporting material is no longer accessible. | The system explains that the source cannot be displayed and does not substitute unverified information. | Ends with a source-unavailable notification. |

The supporting reference is part of the required behavior. Source-reference functionality remains a known implementation gap for P3.

---

### UC-02 — Organize Assignments

| Field | Description |
|---|---|
| Primary actor | Student |
| Supporting actors and external systems | Learning Management System (Moodle) |
| TUCBW | The student wants to review assignments organized by their due dates. |
| TUCEW | The student sees assignments ordered by due date and can identify an assignment's deadline and submission status, or receives a clear explanation of why the information is unavailable. |
| Preconditions | The student is authenticated and has access to at least one enrolled course. |
| Postconditions | On success, the student sees the available assignments in chronological order with their relevant information. On failure, the student receives an explanation. |
| Traces to requirements | FR-02, FR-04, FR-05, FR-07, QR-02, QR-03, CON-01 |

#### Main Success Scenario

| Actor input/action | System response |
|---|---|
| — | (0) The system presents the student's available courses and indicates that assignment information can be requested. |
| (1) The student requests an organized list of assignments from their enrolled courses. | (2) The system presents the available assignments in ascending order of due date, including course names, due dates, and submission statuses. |
| (3) The student requests more information about a particular assignment. | (4) The system presents the assignment's available instructions, due date, and submission status, and confirms that the assignment details have been provided. |

#### Alternate and Exception Flows

| Flow | At step | Condition | What happens | Ends or rejoins at |
|---|---|---|---|---|
| A1 | 2 | The student has no available assignments. | The system explains that no assignments were found in the student's accessible courses. | Ends with an empty-result acknowledgment. |
| A2 | 2 | One or more assignments have no due date. | The system displays those assignments after all dated assignments and identifies them as having no specified deadline. | Rejoins at step 2. |
| A3 | 2 | Assignment information cannot be retrieved. | The system explains that the requested information is temporarily unavailable and does not present incomplete information as a complete list. | Ends with a retrieval-failure notification. |
| A4 | 4 | The requested assignment is no longer accessible. | The system informs the student that the assignment details are unavailable and offers the available assignment list. | Rejoins at step 1. |

UC-02 describes the required cross-course organization behavior. The prototype can retrieve assignment information, but fully automated cross-course organization remains a development gap.

---

### UC-04 — Generate Practice Questions

| Field | Description |
|---|---|
| Primary actor | Student |
| Supporting actors and external systems | Learning Management System (Moodle) |
| TUCBW | The student wants to practice concepts from an enrolled course. |
| TUCEW | The student receives five course-related practice questions for self-study, or an explanation of why they could not be generated. |
| Preconditions | The student is authenticated and has access to at least one enrolled course. |
| Postconditions | On success, the student has five practice questions based on accessible course material. The student's course records and graded work remain unchanged. On failure, the student receives a clear explanation. |
| Traces to requirements | FR-02, FR-03, FR-07, FR-08, QR-03, QR-04, CON-01 |

#### Main Success Scenario

| Actor input/action | System response |
|---|---|
| — | (0) The system presents the student's available courses and indicates that study questions can be requested. |
| (1) The student selects a course for practice. | (2) The system confirms the selected course and indicates that questions can be generated from its available material. |
| (3) The student requests five practice questions based on the selected course. | (4) The system presents five questions relevant to the course material and confirms that they are intended for self-study rather than graded submission. |

#### Alternate and Exception Flows

| Flow | At step | Condition | What happens | Ends or rejoins at |
|---|---|---|---|---|
| A1 | 4 | The course contains insufficient accessible material to create five relevant questions. | The system explains that there is not enough available course information and does not invent unsupported course content. | Ends with an insufficient-material notification. |
| A2 | 4 | Course information cannot be retrieved. | The system reports that the course material is currently unavailable and that practice questions could not be generated. | Ends with a retrieval-failure notification. |
| A3 | 2 | The selected course is not accessible to the student. | The system explains that the course cannot be accessed and offers the student's available courses. | Rejoins at step 1. |
| A4 | 3 | The student requests questions that would directly complete graded work. | The system declines to complete graded work and offers self-study questions about the relevant concepts instead. | Rejoins at step 3 if the student accepts the alternative. |

This use case specifies expected P3 behavior. The current prototype's tutoring and quiz capabilities do not by themselves establish that the complete practice-question workflow has been verified.

## 4.3 Self-Review Log

The following review records checks made against the P1 use cases, the expanded scenarios above, and the Lesson 13 criteria in the P2 template.

| Use case | Check from Lesson 13 | Defect found | How it was fixed |
|---|---|---|---|
| UC-01 | Step (0) must describe the initial observable system state. | The P1 scenario began directly with selecting a course. | Added step (0), presenting the student's available courses before an action occurs. |
| UC-01 | Alternate flows must account for normal and exceptional conditions. | The P1 scenario addressed missing information and retrieval failure but did not explicitly cover a selected course being inaccessible. | Added an access-denied alternate flow with a return to course selection. |
| UC-01 | The final response must be observable and satisfy the postcondition. | Supporting-source behavior needed a clearer ending. | Added an observable response identifying the supporting material and confirming its location. |
| UC-02 | Each interaction must identify the student's action and system response. | The P1 flow mixed student actions with internal sorting activities. | Rewritten as paired actor/system interactions focused on what the student requests and sees. |
| UC-02 | A condition that may be false during normal operation belongs in an alternate flow. | Assignments may have no due date, and some students may have no assignments. | Preserved explicit alternate flows for missing due dates and empty assignment lists. |
| UC-02 | A use case must end with a perceivable result. | The P1 scenario ended after displaying an organized list without a detailed follow-up response. | Added an assignment-detail response that confirms the requested details were provided. |
| UC-04 | The use case must have a defined start, end, and postconditions. | UC-04 was not expanded in the provided P1 document. | Defined the trigger, end condition, preconditions, and success/failure postconditions. |
| UC-04 | Exception flows must be described. | No detailed exception flows were available in the P1 document. | Added insufficient-material, retrieval-failure, unauthorized-course, and graded-work-request alternatives. |
| All three | Analysis steps must avoid implementation details. | References to internal retrieval and processing appeared in the P1 scenarios. | Rephrased the interactions in terms of student requests and observable responses. |
| All three | Every analyzed use case must trace to functional requirements. | Inconsistent UC-04/UC-05 identifiers appeared in the P1 traceability matrix. | Used the consolidated Section 3.4 numbering and included functional requirement references for each expanded use case. |

The cross-author domain-model and sequence-diagram checks belong to Section 5.3 and must be completed after Omor and Daniel finish their models.
