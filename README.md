# LMS Study Assistant

A command-line study assistant for **students**, connected to a self-hosted **Moodle** LMS. It uses Claude (`claude-opus-5-5`) to help a student stay organized and learn the material, using only that student's own data.

Examples:
- "What's due this week?" / "Am I missing anything?"
- "How am I doing in CS101?"
- "What's the late policy?"
- "I don't get the Lab 1 instructions. What's a loop counter?"
- "Quiz me on loops."

It tutors and doesn't do graded work for students: it explains, gives a different worked example, or reviews the student's own attempt. That rule is in `SYSTEM` in `agent.py`, and it follows any AI policy in the course.

## 1. Run the assistant on mock data (no Moodle needed)

```bash
cd lms-agent
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then add your ANTHROPIC_API_KEY
python agent.py
```

## 2. Start Moodle

Needs [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Mac with Apple chip version). Open it once so it's running, then:

```bash
cd lms-agent
docker compose up -d
```

The first start takes a few minutes while Moodle installs itself. Watch progress with `docker compose logs -f moodle`. When it's ready, open http://localhost:8080 and sign in as `admin`, with the password from `MOODLE_ADMIN_PASSWORD` in `.env`.

Stop it with `docker compose down`. Your courses are kept. `docker compose down -v` deletes everything.

## 3a. Quick option: load the sample course

After turning on the API (step 1 below), this creates a sample **CS101** course with weekly pages, four assignments (one graded late, one missing, two upcoming), an announcement, and an enrolled test student. It also saves that student's token in `.env`:

```bash
printf '\nMOODLE_STUDENT_USERNAME=student1\nMOODLE_STUDENT_PASSWORD=Stu-%s!\n' "$(LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c 12)" >> .env
set -a; source .env; set +a
docker compose cp moodle/seed_sample_course.php moodle:/tmp/seed.php
docker compose exec -T -e STUDENT_USERNAME="$MOODLE_STUDENT_USERNAME" -e STUDENT_PASSWORD="$MOODLE_STUDENT_PASSWORD" moodle php /tmp/seed.php
```

Then get the token with `python get_moodle_token.py`, using the student username and password from `.env`.

## 3. Set up Moodle for the assistant (once, as admin)

1. **Turn on the API**: Site administration → General → Mobile app → Mobile settings → check **Enable web services for mobile devices** → Save.
2. **Make a course**: Site administration → Courses → Add a new course. Then add:
   - a course **summary** with syllabus basics (grading, late policy, office hours), or a **Page** called "Syllabus"
   - a couple of **Pages** with notes
   - two or three **Assignments** with due dates, one of them due soon
   - a post in the **Announcements** forum
3. **Make a test student**: Site administration → Users → Add a new user. Then in the course: Participants → **Enrol users** → choose them as **Student**.
4. **Get the student's token**:
   ```bash
   python get_moodle_token.py
   ```
   Enter the student's username and password. Or sign in as the student and copy the "Moodle mobile web service" key from Profile → Preferences → **Security keys**. Put it in `.env` as `MOODLE_TOKEN=...`.
5. Run `python agent.py`. The first line should say `using Moodle (...)`.

## 4. Chat bubble in Moodle (no terminal for students)

Students can chat from a bubble in the corner of every Moodle page.

1. Start the web server (leave it running):
   ```bash
   python server.py
   ```
   You can also open the chat page on its own at http://localhost:8000.
2. In Moodle, as admin: **Site administration → Appearance → Additional HTML → "Before BODY is closed"**, paste this and save:
   ```html
   <script src="http://localhost:8000/embed.js"></script>
   ```
3. Sign in to Moodle as a student. A blue chat button appears at the bottom right of every page. It's hidden on the login page and for visitors who aren't signed in.

**Prototype limits:** every chat uses the one student token in `.env`, so everyone who opens the bubble sees that student's data. Chats are kept in memory and cleared when the server restarts. For real students, the next step is LTI 1.3, so Moodle tells the assistant who is signed in. If teammates should use your server, set `AGENT_HOST=0.0.0.0` and point the script tag at your Tailscale address instead of `localhost`. Anyone who can reach the server uses your Anthropic API credits.

## Team access

**Code:** put this folder in a private GitHub repo (`.env` is git-ignored, so keys and passwords stay out). Teammates clone it, make their own `.env`, and run the agent on their own computer. Anyone can edit `agent.py` and `lms.py` and open pull requests.

**Moodle:** there are two ways for teammates to use it:
- **Each person runs their own copy** with `docker compose up -d`. This is best for development, because nobody blocks anyone. Course content isn't shared between copies.
- **Everyone shares the Moodle on this Mac.** Install [Tailscale](https://tailscale.com) (free) on this Mac and each teammate's computer, and invite them to your tailnet. Then set both `MOODLE_SITE_URL` and `MOODLE_URL` in `.env` to this Mac's Tailscale address (e.g. `http://johns-macbook-pro:8080`), and run `docker compose up -d` again. Teammates set `MOODLE_URL` to the same address. This Mac has to be on, awake and running Docker for this to work.

`MOODLE_SITE_URL` must match exactly what people type in the browser, or Moodle redirects them to the wrong address.

## How it works

| File | What it does |
|---|---|
| `agent.py` | Chat loop, the tutor's instructions (`SYSTEM`), and tool definitions. |
| `lms.py` | `MoodleLMS` (Moodle web service API) and `MockLMS` (sample data), with the same methods. |
| `docker-compose.yml` | Moodle 5.3 + PostgreSQL. |
| `server.py` | Web server: chat page at `/`, Moodle bubble script at `/embed.js`, chat API at `/api/chat`. |
| `web/` | The chat page (`chat.html`) and Moodle bubble (`embed.js`). |
| `get_moodle_token.py` | Gets a student's API token. |
| `sample_data.json` | Fake course from one student's point of view. |

Tools (all read-only): `list_my_courses`, `list_my_assignments`, `get_assignment`, `get_syllabus`, `list_modules`, `get_page`, `list_announcements`.

## Adding a tool

1. Find the Moodle function at http://localhost:8080/admin/webservice/documentation.php. It must be in the mobile app service.
2. Add a method to both `MoodleLMS` and `MockLMS` in `lms.py`.
3. Add a matching entry to `TOOLS` in `agent.py`.
4. If it changes anything (submitting work, messaging a teacher), add its name to `NEEDS_APPROVAL` so the student confirms first.
