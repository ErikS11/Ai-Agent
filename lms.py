"""LMS clients for a student-facing assistant: a real Moodle client and an offline mock.

Every method returns only what the signed-in student can see about themselves
and their courses. The Moodle token decides whose data that is.
"""

import json
import os
import re
import time
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

import requests


def html_to_text(html: str | None) -> str:
    """Moodle content is HTML; strip tags so Claude gets readable text."""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html or "", flags=re.S | re.I)
    text = re.sub(r"<br\s*/?>|</p>|</li>|</h\d>", "\n", text, flags=re.I)
    text = unescape(re.sub(r"<[^>]+>", "", text))
    return re.sub(r"\n\s*\n+", "\n\n", text).strip()


def iso(ts: int | None) -> str | None:
    """Moodle uses Unix timestamps; 0 means 'not set'."""
    return datetime.fromtimestamp(ts, timezone.utc).isoformat() if ts else None


def _flatten(params: dict, prefix: str = "") -> dict:
    """Moodle REST wants lists/dicts as courseids[0]=2, options[0][name]=x, ..."""
    out = {}
    for k, v in params.items():
        key = f"{prefix}[{k}]" if prefix else str(k)
        if isinstance(v, dict):
            out.update(_flatten(v, key))
        elif isinstance(v, (list, tuple)):
            out.update(_flatten(dict(enumerate(v)), key))
        elif isinstance(v, bool):
            out[key] = int(v)
        else:
            out[key] = v
    return out


class MoodleLMS:
    """Wrapper over Moodle's web service API, using the student's mobile-app token.

    Function reference: <your Moodle>/admin/webservice/documentation.php
    """

    def __init__(self, base_url: str, token: str):
        self.url = base_url.rstrip("/") + "/webservice/rest/server.php"
        self.token = token
        self._userid = None

    def _call(self, function: str, **params):
        data = {"wstoken": self.token, "wsfunction": function, "moodlewsrestformat": "json", **_flatten(params)}
        r = requests.post(self.url, data=data, timeout=30)
        r.raise_for_status()
        result = r.json()
        # Moodle reports errors as HTTP 200 with an "exception" field.
        if isinstance(result, dict) and "exception" in result:
            raise RuntimeError(f"Moodle {function}: {result.get('message')}")
        return result

    @property
    def userid(self) -> int:
        if self._userid is None:
            self._userid = self._call("core_webservice_get_site_info")["userid"]
        return self._userid

    def list_my_courses(self):
        courses = self._call("core_enrol_get_users_courses", userid=self.userid)
        try:
            grades = {g["courseid"]: g.get("grade") for g in
                      self._call("gradereport_overview_get_course_grades")["grades"]}
        except Exception:
            grades = {}
        return [{"id": c["id"], "name": c["fullname"], "code": c["shortname"],
                 "current_grade": grades.get(c["id"])} for c in courses]

    def _assignments(self, course_id: int) -> list:
        courses = self._call("mod_assign_get_assignments", courseids=[course_id])["courses"]
        return courses[0]["assignments"] if courses else []

    def list_my_assignments(self, course_id: int):
        out, now = [], time.time()
        for a in self._assignments(course_id):
            status = self._call("mod_assign_get_submission_status", assignid=a["id"])
            sub = (status.get("lastattempt") or {}).get("submission") or {}
            grade = ((status.get("feedback") or {}).get("gradefordisplay"))
            submitted = sub.get("status") == "submitted"
            due = a.get("duedate") or 0
            out.append({
                "id": a["id"],
                "name": a["name"],
                "due_at": iso(due),
                "max_grade": a.get("grade"),
                "my_status": sub.get("status", "new"),
                "my_grade": html_to_text(grade) if grade else None,
                "late": bool(submitted and due and sub.get("timemodified", 0) > due),
                "missing": bool(not submitted and due and due < now),
            })
        return out

    def get_assignment(self, course_id: int, assignment_id: int):
        for a in self._assignments(course_id):
            if a["id"] == int(assignment_id):
                return {"name": a["name"], "due_at": iso(a.get("duedate")),
                        "max_grade": a.get("grade"), "instructions": html_to_text(a.get("intro"))}
        raise ValueError(f"No assignment with id {assignment_id}")

    def get_syllabus(self, course_id: int):
        c = self._call("core_course_get_courses_by_field", field="id", value=course_id)["courses"][0]
        return {"course": c["fullname"], "summary": html_to_text(c.get("summary")),
                "note": "Instructors may also post the full syllabus as a page; check list_modules."}

    def list_modules(self, course_id: int):
        sections = self._call("core_course_get_contents", courseid=course_id)
        return [
            {
                "name": s.get("name"),
                "items": [{"title": m["name"], "type": m["modname"],
                           "page_id": str(m["id"]) if m["modname"] == "page" else None}
                          for m in s.get("modules", []) if m.get("uservisible", True)],
            }
            for s in sections
        ]

    def get_page(self, course_id: int, page_id: str):
        for p in self._call("mod_page_get_pages_by_courses", courseids=[course_id])["pages"]:
            if str(p["coursemodule"]) == str(page_id):
                return {"title": p["name"], "body": html_to_text(p.get("content"))}
        raise ValueError(f"No page with id {page_id}")

    def list_announcements(self, course_id: int):
        forums = self._call("mod_forum_get_forums_by_courses", courseids=[course_id])
        news = next((f for f in forums if f.get("type") == "news"), None)
        if not news:
            return []
        posts = self._call("mod_forum_get_forum_discussions", forumid=news["id"], page=0, perpage=10)
        return [{"title": d.get("name") or d.get("subject"), "posted_at": iso(d.get("created")),
                 "message": html_to_text(d.get("message"))} for d in posts.get("discussions", [])]


class MockLMS:
    """Offline stand-in backed by sample_data.json: one student's view of one course."""

    def __init__(self, path: Path = Path(__file__).with_name("sample_data.json")):
        self.data = json.loads(path.read_text())

    def _course(self, course_id: int) -> dict:
        for c in self.data["courses"]:
            if c["id"] == int(course_id):
                return c
        raise ValueError(f"No course with id {course_id}")

    def list_my_courses(self):
        return [{k: c[k] for k in ("id", "name", "code", "current_grade")} for c in self.data["courses"]]

    def list_my_assignments(self, course_id: int):
        return [{k: v for k, v in a.items() if k != "instructions"}
                for a in self._course(course_id)["assignments"]]

    def get_assignment(self, course_id: int, assignment_id: int):
        for a in self._course(course_id)["assignments"]:
            if a["id"] == int(assignment_id):
                return {k: a[k] for k in ("name", "due_at", "max_grade", "instructions")}
        raise ValueError(f"No assignment with id {assignment_id}")

    def get_syllabus(self, course_id: int):
        c = self._course(course_id)
        return {"course": c["name"], "summary": c["syllabus"]}

    def list_modules(self, course_id: int):
        return self._course(course_id)["modules"]

    def get_page(self, course_id: int, page_id: str):
        pages = self._course(course_id)["pages"]
        if page_id not in pages:
            raise ValueError(f"No page with id {page_id}")
        return pages[page_id]

    def list_announcements(self, course_id: int):
        return self._course(course_id)["announcements"]


def make_lms():
    """Use Moodle when MOODLE_URL and MOODLE_TOKEN are set, otherwise the mock."""
    base, token = os.getenv("MOODLE_URL"), os.getenv("MOODLE_TOKEN")
    if base and token:
        return MoodleLMS(base, token), f"Moodle ({base})"
    return MockLMS(), "mock data (set MOODLE_TOKEN in .env to use Moodle)"
