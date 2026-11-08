# Team Onboarding: LMS AI Agent (Group 1)

Start here. This covers what we've built so far, how to run it on your computer, and how to contribute.
**For P2 (due Sun Nov 8, 11:59 PM), go straight to [docs/p2/WORK_PLAN.md](docs/p2/WORK_PLAN.md) after setup.**

## 1. Where the project is

| | P1 said | Now |
|---|---|---|
| LMS | Canvas (self-hosted) | **Moodle 5.3, self-hosted in Docker.** Canvas's free version (Canvas Lite) blocks API tokens for every account, so the agent couldn't connect |
| Agent | Planned | **Working.** A student asks in plain English, and Claude answers using 7 read-only tools that read only that student's own Moodle data |
| Where students use it | Not decided | **A chat bubble on every Moodle page**, plus a terminal version for testing |
| Sample data | Planned | **CS101 course** with pages, 4 assignments (one late, one missing, two upcoming), an announcement and a test student |

What the agent can do today: list your courses and current grade, what's due and what's missing, assignment instructions, the syllabus and late policy, course pages and notes, and announcements. It also tutors and quizzes you. It **won't** do graded work for you, and it never changes anything in Moodle.

### How the pieces fit

```
 Student's browser
 ├── Moodle pages ──────────── HTTP :8080 ──► Moodle 5.3 (Docker) ──► PostgreSQL (Docker)
 └── Chat bubble (iframe) ──── HTTP :8000 ──► Agent server (server.py, FastAPI)
                                                 └── Agent core (agent.py)
                                                      ├── LMS adapter (lms.py) ── Moodle web services (REST, student token) ──► Moodle
                                                      └── Claude API (HTTPS) ──► Anthropic   ← data leaves our machine here
```

| File | What it is |
|---|---|
| `agent.py` | Agent core: system prompt (tutor rules), the 7 tool definitions, the loop that runs tools until Claude answers. `python agent.py` = terminal chat |
| `lms.py` | `MoodleLMS` (real Moodle API) and `MockLMS` (reads `sample_data.json`, no Moodle needed) |
| `server.py` | Web server: chat page at `/`, bubble script at `/embed.js`, chat API at `POST /api/chat` |
| `web/chat.html`, `web/embed.js` | Chat panel and the Moodle bubble |
| `docker-compose.yml` | Moodle + PostgreSQL |
| `moodle/seed_sample_course.php` | Creates the CS101 sample course and test student |
| `get_moodle_token.py` | Gets a student's API token |
| `docs/p2/` | P2 work plan, section files, diagrams |

## 2. Set up on your computer (about 20 minutes)

You need: **Git**, **Python 3.11+**, **Docker Desktop**, a **GitHub account with write access** to this repo (ask Ahmad, `azghier1`), and an **Anthropic API key** (create your own at console.anthropic.com, or get one from John privately. **Never paste a key into the repo or the group chat**).

> **Only working on the P2 document?** You just need steps 1 and 6. Steps 2 to 5 are for running the app (useful for writing accurate sections, required for Zaid's spike).

**1. Clone**
```bash
git clone https://github.com/azghier1/Ai-Agent.git
cd Ai-Agent
```

**2. Python environment**
```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # Windows: copy .env.example .env
```
Open `.env` and set `ANTHROPIC_API_KEY`. Make up a `MOODLE_ADMIN_PASSWORD` (e.g. `Mdl-` + 12 random letters + `!`).

**3. Try it with no Moodle (fake course)**
```bash
python agent.py
```
Ask "Am I missing anything?". It should mention a missing reading reflection. Type `quit` to exit.

**4. Start Moodle** (Docker Desktop must be open)
```bash
docker compose up -d
```
Wait 1 to 3 minutes, then open http://localhost:8080 and log in as `admin` with your `MOODLE_ADMIN_PASSWORD`. Then:
- Go to http://localhost:8080/admin/settings.php?section=mobilesettings, check **Enable web services for mobile devices**, and click **Save**.
- Load the sample course (Mac/Linux shell; on Windows use Git Bash):
  ```bash
  printf '\nMOODLE_STUDENT_USERNAME=student1\nMOODLE_STUDENT_PASSWORD=Stu-%s!\n' "$(LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c 12)" >> .env
  set -a; source .env; set +a
  docker compose cp moodle/seed_sample_course.php moodle:/tmp/seed.php
  docker compose exec -T -e STUDENT_USERNAME="$MOODLE_STUDENT_USERNAME" -e STUDENT_PASSWORD="$MOODLE_STUDENT_PASSWORD" moodle php /tmp/seed.php
  ```
- Get the student's token with `python get_moodle_token.py` (username `student1`, password from `MOODLE_STUDENT_PASSWORD` in `.env`) and paste it into `.env` as `MOODLE_TOKEN=...`.
- Run `python agent.py` again. The first line should now say `using Moodle (http://localhost:8080)`.

**5. Chat bubble in Moodle**
```bash
python server.py
```
In Moodle as admin, go to **Site administration → Appearance → Additional HTML → "Before BODY is closed"**, paste `<script src="http://localhost:8000/embed.js"></script>` and save. Log out, then log in as `student1`. The blue chat button is at the bottom right.

Stop Moodle with `docker compose down` (your data is kept).

**6. Git workflow (this is how we get graded)**

```bash
git checkout main && git pull                       # always start from the latest main
git checkout -b docs/p2-section-6                   # branch name: type/short-description
# ...edit your files...
git add docs/p2/sections/6-design.md docs/p2/diagrams/component-view.drawio
git commit -m "6.3: add component view"             # message starts with the section or requirement
git push -u origin docs/p2-section-6
```
Then on GitHub, click **Compare & pull request**, add your reviewer from the work plan, and wait for their approval before you merge.

Rules (from our P1 section 4.4):
- `main` only gets reviewed work. Everything goes through a pull request, and someone else approves it.
- Commit messages start with the section or requirement: `4.2: expand UC-01`, `FR-03: tighten acceptance test`.
- Commit **from your own account**. Your commits and reviews are your individual grade.
- **Never commit `.env`**, API keys or passwords. `.gitignore` already blocks `.env`, so don't override it.
- Used an AI tool? Tell John so it goes in 10.5. Commits with an AI co-author line must be declared there.

## 3. Common problems

| Problem | Fix |
|---|---|
| `Auth failed: set ANTHROPIC_API_KEY` | Key missing or wrong in `.env` |
| Moodle page won't load | `docker compose ps`: both containers should be `Up`. Check `docker compose logs moodle` |
| `Moodle ...: Invalid token` | Token missing or wrong, or mobile web services not enabled (step 4) |
| Bubble says it can't reach the assistant | `python server.py` isn't running |
| `git push` asks for a password | Use a GitHub **personal access token** (Settings → Developer settings → Tokens (classic), scope `repo`), not your password |
| Permission denied on push | Ask Ahmad to add you as a collaborator |
