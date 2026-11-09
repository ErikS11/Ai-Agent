# 1 Introduction

## 1.1 Purpose of this document and of the system

This document is the P2 analysis and high-level design baseline (version 1.0) for the LMS AI Agent, written by Group 1 (Section 010) for the CS 3354 instructor and teaching assistants, and for the team as the reference that P3 implementation and testing will trace back to. It carries forward the P1 problem, scope and requirements under change control (section 0.2) and adds use-case analysis, analysis models, the architecture and its rationale.

The LMS AI Agent is a study assistant for students that works on top of a learning management system. A student's course information is spread across modules, pages, announcements and assignment pages in every course they take, and the LMS gives no way to ask a plain-language question about that material or to see what is due at a glance. The agent lets a signed-in student ask questions answered only from their own enrolled courses' material, see their assignments and what is due soon, and practice with generated questions.

For development and testing the team runs its own instance of Moodle 5.3, an open-source LMS, loaded with sample course data. P1 planned on Canvas; the free hosted Canvas blocks the API access the agent needs, so the team moved to Moodle (CH-02, ADR-02). The problem belongs to students; the office that runs a university's LMS has a stake in keeping any such agent inside the access a student already has.

## 1.2 Scope

| In scope: we will build this | Out of scope: we will not, and why |
|---|---|
| Answering students' natural-language questions using only the material in courses they are enrolled in (FR-01 to FR-03) | Answers drawn from the open web or from courses the student is not enrolled in: we cannot vouch for accuracy, and it would reach past the student's own access |
| Retrieving a student's assignments and submission status from the LMS, sorted by due date, with the next seven days flagged (FR-04 to FR-06) | Submitting, editing or deleting any work in the LMS on a student's behalf: the agent only reads; writing raises academic-integrity and approval issues |
| Generating practice questions from course material (FR-08) | Completing graded assignments or quizzes for students: this would be academic dishonesty, not study help |
| Clear error messages when LMS data cannot be retrieved (FR-07), with each student identified through their own LMS sign-in | Instructor and administrator features such as grading, course setup or analytics, and support for more than one LMS: we have one term and one user class to serve well |

Unchanged since v0.5 except for the LMS named in the last row (CH-02, CH-10).

## 1.3 Definitions, acronyms and abbreviations

| Term or abbreviation | Meaning as used in this project |
|---|---|
| LMS | Learning Management System: the platform a university uses to deliver courses |
| Moodle | Open-source LMS. The team self-hosts Moodle 5.3 for development and testing (CON-01) |
| Canvas | The LMS used at UT Dallas, built by Instructure. Named in P1; replaced by Moodle for this project (CH-02) |
| Moodle web services | Moodle's interface for other software to read course data on behalf of a signed-in user |
| AI agent | Our system: software that takes a student's request, retrieves the data it needs from the LMS, and uses a large language model to produce an answer or list |
| LLM | Large language model: the AI model that writes the agent's answers and practice questions |
| Course material | Content a student can already see in an enrolled course: modules, pages, announcements and assignment descriptions. Excludes other students' work and anything hidden from the student |
| Grounded answer | An answer built only from course material, or an explicit statement that the material does not contain enough information (FR-03) |
| Practice question | A question generated from course material for self-study; it is never submitted or graded in the LMS (FR-08) |
| Verified student | A student who has signed in to the LMS and is enrolled in the course being asked about (FR-02, QR-03) |
| LTI 1.3 | Learning Tools Interoperability: the standard way an LMS launches an external tool and tells it who the signed-in user is. Planned for P3 (ADR-05) |
| QAS | Quality-attribute scenario: a measurable quality goal used to drive the architecture (section 6.1) |
| ADR | Architecture decision record: a design decision with its alternatives and cost (section 7) |
| Spike | A small, time-boxed experiment that answers a design question with a measured result (section 8) |
| FERPA | Family Educational Rights and Privacy Act: the U.S. law protecting student education records such as grades and submissions [R4] |
| SSO | Single Sign-On: the campus login service students already use |

## 1.4 References

[R1] ISO/IEC/IEEE 29148:2018, Systems and software engineering, Life cycle processes, Requirements engineering.
[R2] Moodle HQ, Moodle 5.3 web services and external functions documentation.
[R3] UT Dallas OIT, campus single sign-on and Duo two-factor authentication guidance.
[R4] Family Educational Rights and Privacy Act (FERPA), 20 U.S.C. § 1232g; 34 CFR Part 99.
[R5] CS 3354 Fall 2026 syllabus, P1 project brief and P2 project description.
[R6] Anthropic, Claude API documentation (Messages API, tool use).
[R7] 1EdTech, Learning Tools Interoperability (LTI) 1.3 specification.
