# M00 content: Onboarding and Setup (Week 0)

Topic-based teaching content for Week 0. This file is the source for the rebuilt Week 0 deck (M00-DECK-REBUILD), the practical (M00-PRAC), the instructor notes (M00-NOTES) and the self-paced pieces (M00-SELF-PACED: Bash lesson, SQL self-check, setup video script). Those are built only after Daniel approves this file (gate G5).

| Field | Value |
|---|---|
| Work item | M00-CONTENT (Week 0 content file) |
| Author | Claude, 2026-10-07 |
| Reviewer | Codex (G4), then Daniel (G5) |
| Scope authority | `CURRICULUM.md` Week 0, lines 225 to 270 (Big question, 5 objectives, Concepts, Tools, self-paced materials, live session, Practical 0, watch-outs) |
| Evidence used | `source-map.md` (blob 8bb746100aa1), `evidence/notes.md` (blob fdb7092193c2), `evidence/videos.md` (blob 073c07c6291a), `evidence/m00-r6-walkthrough.md` (blob 7137c5f6e992), all at main 34ed3be |
| Code checkpoint | Tag `m00` (58d83c0) and branch `start-m00` (71697f0), rebuilt for Python 3.12 on 2026-10-11, same files: `scripts/verify_setup.sh`, `scripts/check_identity.py`, `scripts/run_notebook.py`, `README.md`, `requirements.in`, `.gitattributes`, `.gitignore`, `data/raw/diamonds.csv` |
| Research gate | G3: M00-RESEARCH (Week 0 research) merged in PR #25 at b21cbaa (head 4827e32) |

## How to read this file

- Topics follow the order a student meets them during setup. They are not slides.
- Each topic has the same 7 parts: objective, explanation, diamond example, limits and common mistakes, diagram spec, demo and practical link, sources.
- Every claim carries one of these labels:
  - **[source]** a named source that the evidence files record as read-full, read-part (with range), visual-checked or doc-verified.
  - **[synthesis]** our own combination of named sources.
  - **[decision]** a course design choice, with the reason.
  - **[fictional]** an invented teaching example.
  - **[measured]** a result produced by running code or by Daniel's live check, with the command and revision.
- "notes A #n" means `evidence/notes.md` Part A, row n. "R6" means Daniel's live AWS check in `evidence/m00-r6-walkthrough.md`.
- Slides carry InnovatiCS branding and no source credits. The citations here are internal.
- Week 0 is mostly official setup pages and our own `m00` build. Psitron adds only contrast (it installs everything natively on Windows). No Psitron text is reused.

**Facts checked this run (2026-10-07, raw pages with curl, label doc-verified 2026-10-07):**
- AWS CLI v2 CHANGELOG (`raw.githubusercontent.com/aws/aws-cli/v2/CHANGELOG.rst`), release 2.36.50: after `aws configure`, the CLI may ask whether to install the "Agent Toolkit for AWS". It appears only when a supported AI coding agent is detected and no AWS skills are installed. Answering `never`, or setting `AWS_CLI_AGENT_TOOLKIT_HINT_DISABLED=true`, turns it off for good. This explains the prompt Daniel saw in R6 (finding 4).
- packages.ubuntu.com: Ubuntu 22.04 (jammy) ships `python3` 3.10.6; Ubuntu 24.04 (noble) ships 3.12.3. Neither ships 3.11.
- deadsnakes PPA on Launchpad: `python3.11` 3.11.17 is published for jammy and noble. (Before the Python 3.12 switch. The course no longer uses this PPA.)
- packages.ubuntu.com: `sqlite3` 3.45.1 is in noble.

**Facts checked for the Python 3.12 switch (2026-10-11, label doc-verified 2026-10-11):**
- Microsoft WSL `distributions/DistributionInfo.json` (github.com/microsoft/WSL): the default `Ubuntu` now installs Ubuntu 26.04.1, which ships Python 3.14 and has no 3.12 package. `Ubuntu-24.04` installs the Ubuntu 24.04.5 LTS image.
- packages.ubuntu.com: Ubuntu 24.04 (noble) ships `python3` 3.12.3, `python3.12` 3.12.3-1ubuntu0.17 (noble-updates) and `python3-venv` 3.12.3-0ubuntu2.1. No PPA is needed.
- Ubuntu 24.04's patched `/usr/lib/python3.12/venv/__init__.py`: without the venv package, `python3.12 -m venv` prints "The virtual environment was not created successfully because ensurepip is not available. On Debian/Ubuntu systems, you need to install the python3-venv package ..."
- python.org: the last Python 3.12 release with a macOS installer is 3.12.10 (April 8, 2025), "macOS 64-bit universal2 installer". 3.12.11 and later are source-only security releases ("No installers").

**Measured on `m00` this run** (`git archive m00 diamond-mlops`, Linux x86_64, 2026-10-07): `diamonds.csv` has 53,941 lines; cut counts Ideal 21,551, Premium 13,791, Very Good 12,082, Good 4,906, Fair 1,610; the 3 scripts are stored without the execute bit (mode 100644), so `./scripts/verify_setup.sh` fails with "Permission denied" (exit 126) and `bash scripts/verify_setup.sh` runs. SQL results are in Topic 11.

**The diamond numbers used in this file** [measured]: HistGradientBoosting, seed 42, 10,755 holdout rows: MAE 279.292629032577, RMSE 524.9243546483148, R2 0.982563973914643. Measured from a clean hash-locked install at `m00` on 2026-10-05 (notes Part C), before the Python 3.12 switch. Re-measured 2026-10-11 on Ubuntu 24.04.5 LTS, Python 3.12.3, clean `git archive m00`: same three values. AGENTS.md section 10 holds the reference values; the runner's tolerance is 1e-9.

---

## Topic 1. Why Week 0 exists, and how the course runs

**Objective.** Students know what the course is, how one week works, and that Week 0 has one goal: a machine that passes 3 checks. (Supports the Big question.)

**Explanation.**
- This is an operations course. Students do not learn to build better models. They learn to take one working model and make it reproducible, testable, deployable and watched. [source: CURRICULUM section 1; syllabus v2 lines 33 to 55, read-part]
- One running example for 14 weeks: Diamond Price Prediction. The code lives in one repo and grows by one practice per week. Week 0 adds nothing to it. Students only prove they can run it. [source: CURRICULUM Week 0 "Diamond repo after this week"; `m00` README lines 1 to 5]
- Week 0 exists so setup problems do not eat Week 1. The planning record says Module 0 was added to stop week-1 dropout. [source: `00_PROJECT_FOUNDATION_and_Decisions.md` line 42, read-part]
- How a week works: prepare before the live session (short readings or videos), one live session of about 3.5 hours, then a practical and a quiz. Week 0 is different: about 3 hours self-paced, then one 90-minute live troubleshooting session. [source: CURRICULUM section 3 and Week 0 Format]
- Grading: quizzes 10%, practicals 40%, 2 checkpoints 20%, capstone 30%. Week 0 is pass/fail, has no quiz and does not count toward the grade. Students must pass it before Week 1. [source: CURRICULUM section 3, line 94; PROJECT_STATE Decisions 2026-10-02]
- AI use: follow the course AI-use policy. [source: CURRICULUM section 1, "AI-use policy", line 52]
- Not decided yet, so leave placeholders: session day and time, holiday breaks, recordings, the LMS (`lms.innovatics.ai` for now, Canvas possible). Student materials must not name LMS menus or features. [source: PROJECT_STATE sections 3 and 5; decision: LMS-neutral]

**Diamond example.** Show the Week 0 "before" picture: one folder, one notebook, one CSV, 3 scripts. By Week 12 the same project has a pipeline, an API, a container, CI/CD, cloud resources and monitoring. [source: CURRICULUM section 4 `m00` row, line 116]

**Limits and common mistakes.**
- Do not promise a finished schedule. Dates and the LMS are still open.
- Syllabus v2 says about 10 weeks, Canvas, 8 quizzes and quizzes 20%. All of that is replaced by CURRICULUM. Do not reuse its schedule or grading. [source: source-map section 1]

**Diagram spec: "Where we are".** Already made: `modules/m00-onboarding/img/where-we-are.png` (from the CURRICULUM section 1 flowchart). Week 0 lit, the rest grey. Reuse as is.

**Demo and practical link.** None. This is the 15-minute welcome block of the live session.

**Sources.** CURRICULUM sections 1 to 4 and Week 0 (read-part, lines named above; notes Part B). Syllabus v2 lines 33 to 55 (read-part). Foundation decisions line 42 (read-part, notes Part B). `m00` README lines 1 to 5 (read-full).

---

## Topic 2. One standard environment: why Linux, and why WSL2

**Objective.** Students can explain why the whole class uses one Linux environment, and they keep their work in the right place. (Objective 1; Concept "works on my machine".)

**Explanation.**
- "Works on my machine" means code runs for one person and fails for another, because their computers differ: operating system, paths, Python version, package versions, line endings. A team fixes this by picking one standard environment. Picking it is itself an MLOps practice. [source: syllabus v2 line 161, read-part]
- Why Linux: the tools in this course assume it. Shell scripts, Makefiles, hardcoded `/` paths and Docker volume mounts behave differently on native Windows. Production servers and containers run Linux, so learning there is closer to the real job. [source: syllabus v2 line 161; Zoomcamp `01-intro/README.md` line 25 "Recommended development environment: Linux", read-part]
- The course supports 3 setups: Windows with WSL2 and Ubuntu, macOS terminal, or native Linux. Native Windows is not supported. [source: CURRICULUM Week 0 objective 1; PROJECT_STATE Decisions 2026-07; AGENTS section 10]
- The **tested** path is Windows with WSL2 Ubuntu. AGENTS section 10 requires every command to work there, and it is what most students (and all EWA students) will use. Native Ubuntu uses the same commands without the WSL steps. The macOS differences are listed in Topic 12; they are doc-checked but **not yet tested on a Mac**. [decision; see Open items]
- WSL2 (Windows Subsystem for Linux, version 2) runs a real Ubuntu inside Windows. Install it with one command, `wsl --install -d Ubuntu-24.04`, in a terminal opened **as administrator** (right-click, "Run as administrator"), then restart. The install page names PowerShell; Microsoft's setup page says PowerShell or Command Prompt. Either works. Our steps show PowerShell. It needs Windows 10 version 2004 or later (build 19041 or later) or Windows 11. New installs use WSL 2 by default. [source: notes A #1, doc-verified 2026-10-05]
- **Why `-d Ubuntu-24.04`.** A plain `wsl --install` installs the default `Ubuntu`, which is now Ubuntu 26.04 with Python 3.14 and no 3.12 package. The locked packages need Python 3.12, which Ubuntu 24.04 ships. Naming the distribution gives every student the same release. [source: Microsoft WSL DistributionInfo.json, doc-verified 2026-10-11; decision]
- If the install hangs at 0.0%, use `wsl --install --web-download -d Ubuntu-24.04`. [source: notes A #1; "Set up a WSL development environment" (learn.microsoft.com/en-us/windows/wsl/setup/environment), Get started section, doc-verified 2026-10-07, for PowerShell or Command Prompt]
- **Where files live.** Ubuntu has its own disk. Your Linux home folder is `/home/<you>`, written `~`. Windows drives appear under `/mnt/c`. Keep all course work under `~`. Microsoft's page says to keep files in the Linux file system when you work from a Linux command line. [source: notes A #3, doc-verified]
- Why it matters, in real numbers: in Daniel's live check, the hash-locked package install ran in `/mnt/c/Users/...` for over 15 minutes and looked frozen. The same install in `~` took under 1 minute. [measured: R6 finding 2, Daniel, 2026-10-07, one machine]
- Where Psitron's setup differs: Psitron installed everything natively on Windows (AWS CLI MSI, Python Windows installer, checks in `cmd`). Its course index puts the WSL link under "Fixing Docker Issues", so its students met WSL only after Docker broke. We start in Linux on day one to skip that detour. [source: Psitron course docs April to May 2024 lines 13 to 35 and 69 to 71; April 2024 lines 402 to 403, read-part, notes Part B. The "skip the detour" line is our synthesis]

**Diamond example.**
- `diamond-mlops/.gitattributes` forces LF line endings on `*.sh` files. Windows Git can convert them to CRLF, and then bash fails on the script. This is a real Windows-vs-Linux trap, fixed in one line. [source: `.gitattributes` at `m00`, notes Part C]
- The notebook reads `../data/raw/diamonds.csv`, a relative path. It works only when started from the right folder. A first taste of why the course later moves paths into config. [source: notebook cell 3 at `m00`, source-map section 2]

**Limits and common mistakes.**
- **Virtualization off.** Errors 0x80370102 or 0x80070003 mean virtualization is off. Fix: turn on the "Virtual Machine Platform" Windows feature and enable virtualization in the BIOS or UEFI settings. The menu name differs by laptop maker. Very old CPUs without SLAT cannot run WSL 2. Put this first in the troubleshooting guide. [source: notes A #2, doc-verified; CURRICULUM watch-outs]
- Students run `wsl --install` in a normal (not administrator) terminal, and it fails or asks for rights. Open the terminal with "Run as administrator". [source: notes A #1]
- Students type a plain `wsl --install` from an older guide and get Ubuntu 26.04. Then `python3.12` is missing. Fix: `wsl --install -d Ubuntu-24.04` and work in that distribution. [source: DistributionInfo.json, doc-verified 2026-10-11]
- Students clone the repo in `/mnt/c/...` because that is where Windows Explorer shows files. It works, but the install can take 15 times longer or more. [measured: R6; source: notes A #3]
- On a work laptop, IT may block WSL or admin rights. Pilot students' OS and admin rights are still unknown. Fallback (GitHub Codespaces) is decided by Oct 24. [source: PROJECT_STATE section 6 Risks]

**Diagram spec: "Where does my code run?"**
- Meaning: one picture that answers "which side am I on?"
- Elements: a large box "Windows laptop". Inside it, on the left: "VS Code window" and "Docker Desktop". On the right, a box "WSL2: Ubuntu" containing "VS Code Server", "your files: `/home/<you>/innovatics-mlops-bootcamp`", "Python 3.12 `.venv`", "docker CLI". Below Ubuntu, a small grey box "`/mnt/c` = your Windows C: drive (slow for code)".
- Relationships: arrow VS Code window to VS Code Server ("edit here, runs there"). Arrow Docker Desktop engine to docker CLI ("WSL integration").
- Source and adaptation: original drawing, from notes A #1, #3, #4 and #5. No source figure is copied.

**Demo and practical link.** Setup guide steps 1 and 2 (install WSL, open Ubuntu, `cd ~`). Expected: `pwd` prints `/home/<you>`. If not: `cd ~`.

**Sources.** Microsoft Install WSL, Troubleshooting WSL, Working across file systems (doc-verified 2026-10-05, notes A #1 to #3). Syllabus v2 line 161 and Zoomcamp `01-intro/README.md` line 25 (read-part, notes Part B). Psitron course docs (read-part, notes Part B). R6 findings (measured by Daniel 2026-10-07).

---

## Topic 3. VS Code with the WSL extension

**Objective.** Students edit files in VS Code on Windows while the code runs inside Ubuntu. (Objective 2.)

**Explanation.**
- VS Code is installed on Windows. The **WSL extension** (id `ms-vscode-remote.remote-wsl`) puts a small VS Code server inside Ubuntu. The window is on Windows. The terminal, Python, Git and files are all in Linux. [source: notes A #4, doc-verified 2026-10-05]
- How to open a project: in the Ubuntu terminal, go to the folder and type `code .`. Or, in VS Code, run "WSL: Connect to WSL" or "WSL: Reopen Folder in WSL". [source: notes A #4]
- How to check you are on the Linux side: the WSL indicator in the bottom-left corner shows you are connected to WSL. The terminal inside VS Code is then an Ubuntu bash terminal. [source: notes A #4]
- Install VS Code on Windows with "Add to PATH" checked, so `code .` works from Ubuntu. [source: notes A #4]
- Older guides call the extension "Remote - WSL". Same tool. [decision: one aside so students recognize old screenshots; the official page does not state the old name, notes A #4]

**Diamond example.** `cd ~/innovatics-mlops-bootcamp/diamond-mlops && code .`, then run the README commands in the VS Code terminal. [source: `m00` README lines 7 to 8]

**Limits and common mistakes.**
- Opening the folder from Windows Explorer through `\\wsl$`. VS Code then runs on the Windows side, and the Python and terminal are wrong. Always open from Ubuntu or with "Reopen Folder in WSL". [synthesis: notes A #3, #4]

**Diagram spec.** Covered by the Topic 2 diagram.

**Demo and practical link.** Setup guide step 3. Expected: VS Code shows the WSL indicator, and `pwd` in its terminal prints a `/home/...` path.

**Sources.** VS Code "Developing in WSL" (doc-verified 2026-10-05, notes A #4). `m00` README (read-full).

---

## Topic 4. Bash basics (the 60-minute self-paced lesson)

**Objective.** Students move around the terminal and run scripts without fear: folders, files, pipes, `grep`, environment variables, running scripts. (Objective 3.)

**Explanation.** The lesson covers exactly the CURRICULUM line 250 list, grouped in 5 short blocks. Every lab in the course uses the terminal, so this is not optional. [source: CURRICULUM line 250; `Planned_Syllabus_Additions.md` lines 9 to 14, read during P-10 map build]

1. **Where am I, what is here.** `pwd` (print the folder you are in), `ls` and `ls -la` (list, including hidden files such as `.gitignore`), `cd folder`, `cd ..`, `cd ~`, `cd -` (back to the previous folder). [source: Linux cheat sheet "File & Directory Operations", read-full text extract, notes Part B]
2. **Make, copy, move, delete.** `mkdir -p a/b`, `cp`, `mv` (also renames), `rm`. `rm -r` deletes a folder and everything in it with no recycle bin. Read the command twice before Enter. [source: cheat sheet same block, which carries the `rm -rf` warning]
3. **Look inside files.** `cat` (print all), `less` (scroll; `q` quits), `head -3`, `tail -5`, `tail -f` (follow a growing log). [source: cheat sheet "File Content & Manipulation"]
4. **Connect commands.** `|` (pipe) sends one command's output into the next. `>` writes output to a file and replaces it. `>>` adds to the end. `grep text file` prints matching lines; `-c` counts them, `-i` ignores case, `-n` shows line numbers. `wc -l` counts lines. [source: cheat sheet "Text Processing & Search" and "Shell & Scripting"; Missing Semester lecture 1, doc-verified, notes A #21]
5. **Environment and scripts.** `export NAME=value` sets an environment variable for this shell and the programs it starts. `echo $NAME` reads it. `$PATH` is the list of folders the shell searches for commands. `which python3.12` shows which file runs. `chmod +x file` makes a file executable. `./script.sh` runs an executable file in this folder. `bash script.sh` runs any script, executable or not. `history` lists past commands. Ctrl+R searches them. [source: cheat sheet "Shell & Scripting" and "System Information" (`echo $PATH`); Missing Semester lecture 1 for `$PATH`, shebang and `chmod`. `which` is in neither the cheat sheet nor the map's local sources, so its line comes from Missing Semester's exercises, notes A #21]
- Exit codes: every command returns a number when it ends. 0 means success. Any other number means failure. Scripts and CI use this number to decide what happens next. [synthesis: Missing Semester lecture 1; `verify_setup.sh` lines 42 to 46. No local source explains exit codes; source-map section 4 gap]
- `sudo` runs one command as the administrator (root). Ubuntu asks for your Linux password, and the prompt shows no characters while you type. [source: Missing Semester lecture 1 for `sudo`; R6 finding 1 for the silent password prompt]

**Diamond example: the exercises run on `diamond-mlops/` at `m00`.** All answers [measured: 2026-10-07 at `m00`; notes Part C]:
- `head -3 data/raw/diamonds.csv` shows the header `carat,cut,color,clarity,depth,table,price,x,y,z` and two rows priced 326.
- `wc -l data/raw/diamonds.csv` prints 53941: 53,940 diamonds plus 1 header line.
- `grep -c ",Ideal," data/raw/diamonds.csv` prints 21551.
- `cut -d, -f2 data/raw/diamonds.csv | tail -n +2 | sort | uniq -c | sort -rn` counts diamonds per cut: Ideal 21,551, Premium 13,791, Very Good 12,082, Good 4,906, Fair 1,610. A 5-command pipe, read left to right. (`cut`, `sort` and `uniq` are extras beyond line 250; mark this one as a stretch exercise.)
- `cat .gitignore` shows the 7 patterns Git ignores, including `.venv/` and `.env`.
- `ls -l scripts` shows `-rw-` on `verify_setup.sh`: no `x`. So `./scripts/verify_setup.sh` fails with "Permission denied" (exit code 126), and `bash scripts/verify_setup.sh` works. This is why the course always writes `bash scripts/...`. [measured]
- Capstone of the lesson: read `scripts/verify_setup.sh` (46 lines) and find: `command -v aws` (is the tool installed?), the pipe from `aws sts ...` into Python (lines 15 to 18), `failures=$((failures + 1))` (counting), and `exit 1` (tell the caller it failed). [source: `verify_setup.sh` at `m00`, read-full]

**Limits and common mistakes.**
- `>` silently replaces a file. Use `>>` to add.
- `rm -r` has no undo.
- Typing `export` in one terminal does not affect another terminal. Put lasting settings in `~/.bashrc`, then `source ~/.bashrc`. [source: cheat sheet "Shell & Scripting"]
- Skip from the cheat sheet: GRUB, fsck, users and groups, yum or flatpak, iptables, `ifconfig`. They are sysadmin topics. [decision: source-map section 4]
- The LabEx cheat sheet is third-party. Link to it; do not rebrand or hand it out as ours. [decision: source-map section 4]

**Diagram spec: "The pipe".**
- Meaning: data flows left to right through a pipe; `>` catches the end in a file.
- Elements: 3 boxes `cat data/raw/diamonds.csv` then `grep ",Ideal,"` then `wc -l`, joined by `|` arrows. Under each arrow, a tiny sample of what flows: "53,941 lines", "21,551 lines", "21551". A side branch: `> ideal.csv` drawn as an arrow into a file icon.
- Source and adaptation: original drawing; numbers measured at `m00`.

**Demo and practical link.** The lesson ends with 8 to 10 exercises like the ones above, built in M00-SELF-PACED. Expected: students can run `bash scripts/verify_setup.sh` and explain each line it prints. Optional practice links: cmdchallenge.com ("One-line shell challenges", notes A #23) and MIT Missing Semester lecture 1 (the one required external resource).

**Sources.** Linux cheat sheet (read-full text extract; blocks named; notes Part B corrects the map: `echo $HOME` and `echo $PATH` are present, `which` is not). Missing Semester lecture 1 (doc-verified 2026-10-05, notes A #21). `verify_setup.sh` and `diamonds.csv` at `m00` (read-full; measured 2026-10-05 and 2026-10-07).

---

## Topic 5. Python 3.12, virtual environments and locked packages

**Objective.** Students explain why each project gets its own environment and why every package version is locked, and they create the course environment. (Concept: virtual environments; Tools: Python 3.12, `venv`, Jupyter.)

**Explanation.**
- A **virtual environment** (venv) is a folder that holds its own Python packages. Two projects can then need different versions of the same package and not break each other. [source: Python 3.11 venv docs, doc-verified, notes A #18]
- Create: `python3.12 -m venv .venv`. Use: call `.venv/bin/python` directly, or `source .venv/bin/activate` first. Activation is optional; the course commands call `.venv/bin/python` so they work either way. [source: notes A #18; `m00` README lines 14 to 20]
- A venv is disposable and never goes into Git. Delete it and rebuild it any time. That is why `.gitignore` lists `.venv/`. [source: notes A #18; `.gitignore` at `m00`]
- **Why exactly Python 3.12.** The locked packages are resolved for 3.12 on Linux and macOS. The notebook runner refuses any other version and any environment other than the project's `.venv`. [source: `run_notebook.py` line 19; README lines 28 to 31]
- Ubuntu 24.04 ships Python 3.12.3 as its system `python3`, so the course Python is the system Python. Students add only `python3-venv` (`sudo apt install -y python3-venv`). No PPA. Ubuntu 22.04 ships 3.10 and is not supported. Ubuntu 26.04 ships 3.14 and has no 3.12 package, so Windows students install `Ubuntu-24.04` by name (Topic 2). [source: packages.ubuntu.com and Microsoft WSL DistributionInfo.json, doc-verified 2026-10-11]
- **Why lock versions with hashes.** `requirements.in` lists 11 direct packages, each pinned (for example scikit-learn 1.7.2, pandas 3.0.6, numpy 2.4.6). `requirements.txt` locks every package, including the ones those depend on, with a hash. `pip install --require-hashes -r requirements.txt` refuses any file whose hash differs: no silent upgrades and no tampered downloads. Hash mode is all or nothing: every line must be pinned and hashed. [source: pip secure installs, doc-verified, notes A #19; `requirements.in` at `m00`, measured 11 pins, notes Part C]
- The payoff: everyone gets the exact same metrics. A newer scikit-learn changes MAE from 279.29 to 278.16. Without locks, two students would get two different "correct" answers. [source: `diamond-mlops/docs/problem-framing.md` line 66 at tag `m01` (7596237), line re-checked 2026-10-11]
- `pip check` after install confirms no package has a broken dependency. It printed "No broken requirements found." on our run. [measured: notes Part C]

**Diamond example.** The install block, exactly as in `diamond-mlops/README.md` lines 15 to 18 at `m00` (58d83c0):
```bash
cd diamond-mlops
python3.12 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.txt
.venv/bin/python -m pip check
```
- Run it from the clone inside `~`, not under `/mnt/c` (Topic 2). [measured: R6 finding 2]
- Measured on Ubuntu 24.04.5 LTS on 2026-10-11, Python 3.12.3, clean `git archive m00`: this block (with `--no-cache-dir`) and `pip check` took 73 seconds, and `pip check` printed "No broken requirements found." `scripts/run_notebook.py` then passed in 42 seconds with the reference numbers. [measured: see the Python install test below]
- Optional, not part of the tagged block: Daniel added `--no-cache-dir` in R6. It skips a second copy of every package in `~/.cache/pip`. Venv plus cache came to about 649 MB on his machine. Student materials may mention it as a disk-space tip only; the required command stays the tagged one. [measured: R6 finding 3; decision]

**Python install test (Ubuntu 24.04).** [measured: 2026-10-11, Ubuntu 24.04.5 LTS. Not a fresh WSL install; the WSL check stays an open item]
```bash
sudo apt update
sudo apt install -y python3-venv
python3.12 --version
```
- `python3.12 --version` prints `Python 3.12.3`.
- The tagged install block above then passes (73 seconds with `--no-cache-dir`, including `pip check`).
- Before the Python 3.12 switch, a 2026-10-07 test in the `ubuntu:24.04` Docker image installed Python 3.11.17 from the deadsnakes PPA. That path is retired.

**Limits and common mistakes.**
- `make: command not found` in Week 2: the Ubuntu 24.04 WSL image has no `make`. Week 0 Step 3 installs it with the other base tools. [source: `ubuntu-noble-wsl-amd64-wsl.manifest` on cloud-images.ubuntu.com, and packages.ubuntu.com `make` 4.3-4.1build2, doc-verified 2026-10-12]
- `python3.12: command not found`: the machine is not on Ubuntu 24.04 (for example 26.04 from a plain `wsl --install`, or 22.04). Check with `lsb_release -d`. [source: packages.ubuntu.com and DistributionInfo.json, doc-verified 2026-10-11]
- `The virtual environment was not created successfully because ensurepip is not available.` when creating the venv: `python3-venv` is missing. Run `sudo apt install -y python3-venv`, delete the half-made `.venv` with `rm -rf .venv`, and create it again. [source: Ubuntu 24.04 `venv/__init__.py` message, doc-verified 2026-10-11]
- Long quiet periods during the install are normal. Check progress in a second terminal with `du -sh .venv ~/.cache/pip` twice, 30 seconds apart. [measured: R6 finding 3]
- Do not install XGBoost into this environment. The notebook's optional hook would change the winning model and the numbers. [source: README lines 25 to 26]
- Do not use Anaconda. The Zoomcamp setup uses it; we use plain venv and pip. [source: source-map section 5]

**Diagram spec: "Two projects, two environments".**
- Meaning: one system Python, many isolated package sets.
- Elements: one box at the bottom "Python 3.12 (Ubuntu 24.04 system Python)". Above it two project boxes side by side: "diamond-mlops/.venv: scikit-learn 1.7.2, pandas 3.0.6" and "other-project/.venv: scikit-learn 1.4, pandas 2.1" [fictional versions for the second project]. A lock icon on the diamond box labelled "requirements.txt with hashes".
- Source and adaptation: original drawing.

**Demo and practical link.** Setup guide "install the notebook environment". Expected: `pip check` prints "No broken requirements found."

**Sources.** Python venv docs and pip secure installs (doc-verified 2026-10-05, notes A #18, #19). Ubuntu packages and Microsoft WSL DistributionInfo.json (doc-verified 2026-10-11). `m00` README, `requirements.in`, `run_notebook.py` (read-full). R6 findings 2 and 3 (measured by Daniel).

---

## Topic 6. Git identity and GitHub access

**Objective.** Students can clone the course repo and are ready to push in Week 2. (Tools: Git, GitHub account, SSH key.) Git workflow itself is taught in Week 2.

**Explanation.**
- Install Git in Ubuntu with `apt`. Tell Git who you are, once per machine: `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"`. Every commit records this name and email. [source: Git cheat sheet "SETUP" block, read-part, notes Part B. Psitron's Windows installer route is replaced by apt]
- GitHub needs proof that pushes come from you. The course uses an **SSH key**: a key pair. The private key stays on your laptop. The public key goes to GitHub. [decision: CURRICULUM allows SSH key or token; the practical picks SSH, source-map section 6]
- Create the key inside Ubuntu: `ssh-keygen -t ed25519 -C "your_email@example.com"`. Start the agent and add the key: `eval "$(ssh-agent -s)"`, then `ssh-add ~/.ssh/id_ed25519`. Copy the `.pub` file's contents into GitHub settings. Test: `ssh -T git@github.com` replies "Hi USERNAME! You've successfully authenticated...". Use the Linux tab of the GitHub page. [source: GitHub docs, doc-verified, notes A #20]
- Why Git at all, in one line: file names like "report_final.doc" and "report_final_REAL.doc" are manual version control. Git replaces that. Week 2 owns the rest. [fictional file names; the idea follows Psitron M03 Git PDF p6, rendered during the source map build (source-map section 6), rewritten in our words]

**Diamond example.** fork `https://github.com/dislam7991/innovatics-mlops-course`, then `git clone git@github.com:<your-user>/innovatics-mlops-course.git`, then `cd diamond-mlops`.

**Limits and common mistakes.**
- Creating the SSH key on the Windows side. Git inside Ubuntu then cannot see it. Create it in Ubuntu.
- Pasting the private key (no `.pub`) into GitHub. Only the `.pub` file goes to GitHub.
- The Git cheat sheet is from 2014: it shows only `git checkout` and has dead links. Psitron uses `master`. Week 2 teaches `git switch` and `main`. [source: source-map section 6]
- Psitron's Git slide uses a Le Wagon example name and email. Do not copy it. [source: source-map section 6]

**Diagram spec.** Optional: laptop with a key (private), GitHub with a padlock (public), arrow "ssh -T proves they match". Original drawing.

**Demo and practical link.** Setup guide "GitHub SSH". Expected: `ssh -T git@github.com` greets the student by GitHub username.

**Sources.** GitHub SSH docs (doc-verified 2026-10-05, notes A #20). Git cheat sheet (read-part, notes Part B). Psitron M03 Git PDF p6 and p10 (source-map section 6).

---

## Topic 7. Docker Desktop with the WSL2 backend

**Objective.** Students install Docker and prove it runs a container. (Tools: Docker Desktop.) Real Docker teaching is Week 7.

**Explanation.**
- Docker runs software in **containers**: a packaged program plus everything it needs. Week 0 only checks that Docker works. [source: CURRICULUM Week 7 scope; Week 0 Practical 0 check 2]
- On Windows, install Docker Desktop. Its engine runs on WSL 2. It needs WSL version 2.1.5 or later. In Docker Desktop, Settings > Resources > WSL Integration must be on for Ubuntu-24.04; it is on for the default distro. If Docker Engine or the docker CLI was installed inside Ubuntu before, uninstall it first. [source: Docker WSL 2 backend docs, doc-verified, notes A #5]
- On native Linux, install Docker Engine and add yourself to the `docker` group, then log out and back in, or run `newgrp docker`. Without it you see "permission denied ... /var/run/docker.sock". One line of warning: the `docker` group gives root-level power on that machine. [source: Docker Linux post-install, doc-verified, notes A #8; Zoomcamp `01-intro/README.md` lines 39 to 50 and 92 to 98, read-part, which shows the error but not the fix]
- **License.** Docker Desktop is free for personal use, education, non-commercial open source, and businesses with fewer than 250 employees AND less than $10 million revenue. Students on a work laptop at a larger company should check with their employer. [source: Docker Desktop license page, doc-verified 2026-10-05, notes A #6; CURRICULUM watch-outs]
- What `docker run hello-world` does: Docker pulls the image if it is not on the machine, creates a container, runs it, prints a message, and the container exits. By default the stopped container stays on disk. `--rm` deletes it, and its anonymous volumes, when it exits. [source: `docker container run` reference, doc-verified, notes A #7]

**Diamond example.** `verify_setup.sh` line 27 runs `docker run --rm hello-world@sha256:ec1538...`. The `@sha256:` part pins the exact image, the same idea as hash-locked packages. `--rm` leaves nothing behind. [source: `verify_setup.sh` at `m00`, read-full]

**Limits and common mistakes.**
- If check 2 fails on Windows, Docker Desktop is usually not running, or WSL integration is off for Ubuntu-24.04. The script's FAIL line says exactly this (line 30). [source: `verify_setup.sh` line 30; notes A #5]
- Zoomcamp installs `docker.io` from apt and a separate `docker-compose` v2.5.0 binary. Both are old for our setup. Compose is now the `docker compose` plugin. [source: source-map section 7]

**Diagram spec.** None new. Week 7 owns the Docker architecture diagram. The Topic 2 diagram shows where Docker Desktop sits.

**Demo and practical link.** Setup guide "Docker". Expected: `PASS Docker: hello-world completed.` from the verify script.

**Sources.** Docker WSL 2 backend, license, `container run`, Linux post-install (doc-verified 2026-10-05, notes A #5 to #8). Zoomcamp intro README (read-part, notes Part B). `verify_setup.sh` (read-full).

---

## Topic 8. A safe AWS account

**Objective.** Students create an AWS account that cannot surprise them with a bill or a breach: root user locked away with MFA, a budget alert, a least-privilege IAM user, and the AWS CLI configured. (Objective 4; Concepts least privilege and billing alarm.)

**Explanation.**

*8a. Which sign-up path.*
- AWS now offers two sign-up paths. A banner may ask the student to choose. Students choose **"Sign up for AWS (advanced)"**. It creates the classic account the course is built on: a root user, any Region (we use `us-east-1`), and IAM users with access keys. [decision: Daniel, 2026-10-06; source: notes A5 #26, #27, #32]
- The other path, "Sign up for AWS (new)", has no root user, fixes US accounts to us-east-2, and allows IAM users only for programmatic access. It is still rolling out to a limited number of customers. Our materials do not support it. [source: notes A5 #25 to #28]
- Follow only Step 1 of AWS's "Sign up for AWS (advanced)" page. Its Step 2 (`aws login`) gives a root identity right after sign-up, and check 1 rejects root on purpose. Its Step 3 (AWS MCP Server) is out of scope. [source: notes A5 #32; R6 walkthrough Step 1]

*8b. Which plan, and what it costs.*
- Choose the **Free plan**. New accounts get $100 in credits, plus up to $100 more for doing set activities. The Free plan ends after 6 months or when the credits are used up; AWS then suspends the account and erases it after 90 days unless you upgrade. Some services are not available on the Free plan. [source: notes A #17, doc-verified 2026-10-05. Volatile: re-check before launch]
- A Nov 14 start ends about Mar 13, roughly 4 months, so the 6-month limit is not the risk. The risk is credits: the plan ends at whichever comes first, 6 months or credits fully used. A student whose resources burn the credits early loses access before the course ends. [synthesis: PROJECT_STATE section 1; source: AWS "Choosing a plan" (docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html), doc-verified 2026-10-07]
- So say it conditionally: "The account lasts the course **if you do not use up the credits**. Delete what you create the same day (8d) and check your credit balance in the Billing console each week." [decision: Daniel, 2026-10-05, "Free plan until it is absolutely necessary to upgrade, if at all"]
- Recovery path: after the Free plan ends, AWS keeps the content for 90 days. Upgrading to the Paid plan within those 90 days restores access, and any remaining credits apply to future bills. Upgrading early is also allowed. After upgrading, normal pay-as-you-go charges apply, so the budget alert matters more. [source: same AWS page, doc-verified 2026-10-07]
- Do not teach one credit expiry date. AWS's own FAQ says 6 months in some answers and 12 months in others. Safe line: plan on the $100 sign-up credit lasting 6 months. [source: notes A #17]
- **Payment card.** On Daniel's test account (Free plan, advanced path, 2026-10-07), AWS asked for a payment card and said it would hold $1. No SMS check was asked. AWS's pages disagree on whether a card is required. Say exactly that: "AWS asked for a card on our test account; you may or may not be asked." Do not state a rule for all students. [measured: R6, one account; source: notes A5 #32 vs A #17]

*8c. Lock away the root user.*
- The **root user** is the email and password that created the account. It can do anything, including close the account. Use it only for the few tasks that need it. [source: root user best practices, doc-verified, notes A #9]
- First thing after sign-in: turn on **MFA** for root (account menu > Security credentials). AWS now requires root MFA within 35 days of first sign-in anyway. [source: notes A #9]
- **Never create access keys for the root user.** A leaked root key gives a stranger full control of the account. This line goes in bold in every student material. [source: notes A #9; CURRICULUM watch-outs; `m00` README line 37]

*8d. A budget alert, and what it does not do.*
- Create a **monthly cost budget** of $5 with email alerts (AWS Budgets template). Optionally also the **zero spend budget**, which emails after spending goes over the Free Tier limits. [source: AWS budget templates, doc-verified, notes A #11]
- A budget **only sends an email. It does not stop anything.** Budget data updates up to 3 times a day, typically 8 to 12 hours apart, so the email can arrive after the money is spent. [source: AWS Budgets docs, doc-verified, notes A #12]
- So the real protection is a habit: **delete what you create the same day.** Every later practical that creates AWS resources ends with a cleanup step. [source: Zoomcamp best-practices README lines 154 to 158, "destroy infra after use, to avoid costs", read during P-10 map build; decision: course habit]
- Why a budget and not a CloudWatch billing alarm: a CloudWatch billing alarm needs us-east-1, a separate opt-in in Billing preferences, and uses actual charges only (no forecast). The budget template takes one form and can alert on forecast spend. This PR also changes CURRICULUM Week 0 (objective 4, the Concepts line) and the Week 10 cost-management line from "billing alarm" to "budget alert", so the spec and the content agree once Daniel merges it. [source: notes A #11, #13; decision: needs Daniel's merge of this PR]

*8e. An IAM user with no permissions.*
- **Least privilege:** give a user only the permissions it needs. Then a leaked key can do little damage. [source: IAM security best practices, doc-verified, notes A #10]
- Create IAM user `mlops-student`. No console access. **Attach no policies.** Create one access key, use case "Command Line Interface (CLI)". Later weeks add only the permissions that week needs. [source: R6 walkthrough Step 3; decision: Daniel, 2026-10-04, IAM users for students]
- Why no permissions works for Week 0: check 1 calls `aws sts get-caller-identity`. AWS documents that this call needs no permissions at all. It only answers "who am I?" and creates nothing. [source: STS GetCallerIdentity API page, doc-verified, notes A #16; README line 59]
- What real teams do instead: AWS recommends people use short-term credentials, through IAM Identity Center or `aws login`, not long-term IAM user keys. We use one IAM user because it is simpler for a single-person learning account. Say this once so students do not copy the pattern into a company. [source: notes A #10, #15; decision: Daniel, 2026-10-04]

*8f. Configure the AWS CLI.*
- Install AWS CLI v2 with the Linux installer, inside Ubuntu: `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"`, `unzip awscliv2.zip`, `sudo ./aws/install`, then `aws --version`. [source: AWS CLI install page, doc-verified, notes A #14]
- Fresh Ubuntu may lack `unzip`. Run `sudo apt update` and `sudo apt install -y unzip` first. [measured: R6 finding 1, Ubuntu 22.04 in WSL]
- `aws configure` asks 4 questions: Access Key ID, Secret Access Key, default Region (`us-east-1`), output format (`json`). Keys are saved in `~/.aws/credentials`, settings in `~/.aws/config`. Both are in your Linux home folder, outside every repo. [source: notes A #15]
- New CLI versions may then ask whether to install the "Agent Toolkit for AWS" (AWS skills and the AWS MCP server) for an AI coding agent. It appears only when the CLI detects a supported AI coding agent. The course does not use it. Answer `n`, or `never` to stop the question for good. [source: AWS CLI v2 CHANGELOG 2.36.50, doc-verified 2026-10-07; measured: R6 finding 4, Daniel answered n; decision: not used in this course]

*8g. If a key leaks.*
- A key that reaches GitHub, a chat or a screenshot is leaked. In IAM, deactivate the key, create a new one, run `aws configure` again, then delete the old key. Keys live in `~/.aws/credentials` or in a `.env` file that `.gitignore` already excludes, never in code. [source: notes A #10 and Part E item 5; `.gitignore` at `m00`]
- Do not say "AWS tells you to rotate keys every 90 days". AWS's current heading is "Update access keys when needed". [source: notes A #10]
- Do not paste the raw `get-caller-identity` output into chats or tickets. It shows the account ID. The verify script prints only PASS or FAIL. [source: README lines 49 to 50; R6 walkthrough Step 5]

**Diamond example.** `scripts/check_identity.py` accepts only an ARN shaped like `arn:aws:iam::<12 digits>:user/<name>`. Tested with fictional account number 123456789012: an IAM user ARN passes (exit 0); `...:root` fails; an assumed-role ARN fails. So root keys and SSO or role sessions all fail check 1 on purpose. [measured: notes Part C, 2026-10-05]

**Limits and common mistakes.**
- Using root keys "just to get started". The check catches it: the ARN ends in `:root`.
- Expecting the budget to stop spending. It only emails, and can be hours late.
- Picking a different Region in `aws configure`. Later weeks assume `us-east-1`.
- Psitron's sign-up note (INR 2 card charge, Visa or Mastercard, old free tier) is out of date. AWS changed the Free Tier in 2025. [source: notes Part E item 8]
- Zoomcamp uses `eu-west-1` and never says "IAM user, not root". [source: source-map section 8]

**Diagram spec 8-1: "Three layers of AWS access".**
- Meaning: who holds which power, and where the key lives.
- Elements: left, a locked safe "Root user: MFA on, no access keys, used rarely". Middle, "IAM user `mlops-student`: CLI key, no permissions in Week 0, permissions added week by week". Right, a laptop "`~/.aws/credentials` (Linux home, outside every repo)". Under the right box, a crossed-out GitHub logo: "never in Git".
- Relationships: arrow root to IAM user ("creates once"). Arrow IAM user to laptop ("access key").
- Source and adaptation: original drawing from notes A #9, #10, #15.

**Diagram spec 8-2: "The alert comes after the spend".**
- Meaning: a budget alert is a smoke alarm, not a sprinkler.
- Elements: a timeline. Point 1 "you start a resource, 10:00". Point 2 "spend passes $5". Point 3 "AWS Budgets refresh, 8 to 12 hours later". Point 4 "email arrives". A red bracket over points 2 to 4: "money keeps flowing". A green box at point 1: "delete it the same day".
- Source and adaptation: original; timing from notes A #12. The 10:00 start is [fictional].

**Demo and practical link.** Setup guide AWS steps, rebuilt from the R6 walkthrough Steps 1 to 4. Expected: `aws --version` prints `aws-cli/2.x`, and check 1 prints `PASS AWS identity: authenticated as an IAM user.`

**Sources.** AWS root user and IAM best practices, budget templates, Budgets docs, CloudWatch billing alarm, CLI install and config, STS GetCallerIdentity, Free Tier pages (doc-verified 2026-10-05, notes A #9 to #17). Sign-up pages (doc-verified 2026-10-05 and 2026-10-06, notes A5 #25 to #32). AWS CLI CHANGELOG (doc-verified 2026-10-07). R6 (measured by Daniel, 2026-10-07, PR #25 comment 6032122108). `check_identity.py` (read-full, measured).

---

## Topic 9. The verification script and the starting notebook

**Objective.** Students run one command, read its report, and know what each check proves. (Objective 5; the week's Evidence.)

**Explanation.**
- `bash scripts/verify_setup.sh` runs 3 checks and reports each one as PASS or FAIL. It tries all 3 even if one fails, then exits non-zero if any failed. [source: README lines 46 to 47; `verify_setup.sh` lines 7, 22, 31, 39, 42 to 46]
- Before the checks, it needs the project's `.venv`. Without it, it stops at once: "FAIL: create the Python 3.12 .venv and install requirements.txt first." This early stop does not count toward the "N of 3" total. [source: lines 9 to 12; measured: notes Part C and this run]
- **Check 1, AWS identity.** Proves: the AWS CLI is installed, credentials are configured, and they belong to an IAM user (not root, not a role). Creates nothing in AWS. [source: lines 14 to 23; `check_identity.py`; notes A #16]
- **Check 2, Docker.** Proves: Docker is installed, running, reachable from Ubuntu, and can pull and run a pinned image. [source: lines 25 to 32]
- **Check 3, the notebook.** Proves: Python 3.12, the locked packages and the data all work together. It runs every notebook cell in the project's `.venv`, then compares MAE, RMSE and R2 to the reference numbers within 1e-9, and checks the model is HistGradientBoosting with seed 42 and 10,755 holdout rows. It takes several minutes; each cell may run up to 10 minutes. [source: lines 34 to 40; `run_notebook.py` lines 19, 26 to 28, 36, 47 to 56; README lines 53 to 57]
- Why exact numbers and not "it ran": a notebook can run with no error and still give different results on a different package version. Matching the numbers proves the whole class has the same environment. [synthesis: README lines 28 to 31; Topic 5]
- The notebook is also a teaser for Week 1. Its first cell says operations do not belong in a notebook. Its last cell lists what it is not: not tested, not reproducible with one command. Week 1 starts from there. [source: notebook cells 0 and 27 at `m00`, read-full in M01 research]

**Diamond example.** Success ends with:
```
Setup ready: all 3 checks passed.
```
Our run with no AWS CLI and no Docker gave `[1/3]` FAIL, `[2/3]` FAIL, `[3/3]` PASS, then "Setup incomplete: 2 of 3 checks failed." and exit code 1. The notebook check alone took 65 seconds on that machine. [measured: notes Part C, 2026-10-05, at `m00`]

**Limits and common mistakes.**
- `Kernel is running over TCP without encryption` is expected. Look at the final PASS or FAIL line. [source: README lines 72 to 74; measured: notes Part C]
- Running `./scripts/verify_setup.sh` gives "Permission denied". Use `bash scripts/verify_setup.sh`. [measured: Topic 4]
- Running from the wrong folder. The script finds its own project folder (line 4), but `bash scripts/...` must be typed from `diamond-mlops/` for the path to exist.
- Laptops with little memory may be slow on check 3. The runner limits threads to keep memory use predictable. [source: README lines 69 to 70; `run_notebook.py` lines 26 to 28]

**Diagram spec: "Three checks, one green line".**
- Meaning: what each check proves and how it most often fails.
- Elements: 3 boxes in a row: "1 AWS: am I an IAM user?", "2 Docker: can I run a container?", "3 Notebook: do I get the exact diamond numbers?". Each feeds one bar "Setup ready: all 3 checks passed". Under each box, the most likely failure in small text: "root keys, or CLI not configured" / "Docker Desktop not running, or WSL integration off" / "wrong Python, or packages not installed from the lock file".
- Source and adaptation: original drawing from `verify_setup.sh` FAIL lines 21, 30, 38.

**Demo and practical link.** Practical 0 is this command, from a clean clone. Done when all 3 checks pass. The last 10 minutes of the live session: everyone runs it. [source: CURRICULUM Practical 0 and live session]

**Sources.** `verify_setup.sh`, `check_identity.py`, `run_notebook.py`, README at `m00` (read-full; measured notes Part C). Notebook cells 0 and 27 (read-full).

---

## Topic 10. Getting help and reading errors

**Objective.** Students read an error before asking, and ask in a way that gets a fast answer. (Skill: reading error messages; deck plan "where to get help".)

**Explanation.**
- Read the last lines first. Most tools print the real cause at the bottom. Our scripts print what to do next on every FAIL line, for example "start Docker Desktop and enable integration with your WSL2 distro". [source: `verify_setup.sh` lines 10, 21, 30, 38]
- Before asking: search the course FAQ and the existing threads. Someone may have hit the same error. [source: Zoomcamp `asking-questions.md` lines 6 to 18, rewritten]
- When asking, give: what you ran, the full error as **text** (not a screenshot, never a phone photo of the screen), what you already tried, and your setup (Windows with WSL2, macOS or Linux). Keep one problem in one thread. [source: same, rewritten in our words]
- When you fix it, post the fix in the thread. The course FAQ grows from these. [source: same]
- Never paste secrets: no access keys, no passwords, no raw `get-caller-identity` output. [decision: Topic 8g]

**Diamond example.** Two real errors and how to read them:
- "permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock": you are not in the `docker` group (native Linux) or Docker Desktop is not running. [source: Zoomcamp intro README line 98; notes A #8]
- "Permission denied" on `./scripts/verify_setup.sh`: the file is not executable. Use `bash`. A link to `chmod` in Topic 4. [measured: this run]

**Limits and common mistakes.**
- Our help channel is not decided (LMS open). Write "the course help channel"; do not name Slack or an LMS. [decision: LMS-neutral]
- The FAQ does not exist yet. Start it from the practical's troubleshooting table and the Week 0 live session. [source: source-map section 10]

**Diagram spec.** None.

**Demo and practical link.** Live session breakouts (WSL, Docker, AWS) use this format for every question.

**Sources.** Zoomcamp `asking-questions.md` lines 6 to 18 and intro README lines 98, 101 to 105 (read during P-10 map build; not re-opened in M00 research, notes Part B). `verify_setup.sh` (read-full).

---

## Topic 11. SQL self-check (10 minutes, not taught)

**Objective.** Students check they can read simple SQL before Weeks 4, 11 and 12 use it. Nothing new is taught. (Skill: SQL self-check.)

**Explanation.**
- 8 questions on `SELECT`, `WHERE`, `GROUP BY` and `JOIN`. Seven use the diamonds table. The JOIN question uses 2 small separate tables (below), because the diamonds table has nothing to join to. Format: compute a number, then pick the closest option, so it can be auto-graded. [source: CURRICULUM line 251; Zoomcamp 2022 and 2023 HW1 format, read during P-10 map build]
- Run it with Python's built-in `sqlite3` module inside the course `.venv` (no install), or install the `sqlite3` command-line tool with `sudo apt install sqlite3`. [measured: notes Part C, the CLI was not on our image; doc-verified 2026-10-07: `sqlite3` 3.45.1 is in Ubuntu 24.04]
- Anyone who struggles: SQLBolt, interactive lessons in the browser, no sign-up. Do not call it "free"; the site does not say so. [source: notes A #22]

**Diamond example: measured answers on the raw `diamonds.csv`** (before the notebook removes duplicates and zero sizes) [measured: Python `sqlite3`, SQLite 3.45.1, 2026-10-05 and 2026-10-07]:
- `SELECT COUNT(*) FROM diamonds WHERE carat > 2;` gives 1,889.
- `SELECT COUNT(*) FROM diamonds WHERE price > 10000;` gives 5,222.
- `SELECT MAX(price), MIN(price) FROM diamonds;` gives 18,823 and 326.
- Rows with a zero in `x`, `y` or `z`: 20.
- Average price by cut: Premium 4,584.26; Fair 4,358.76; Very Good 3,981.76; Good 3,928.86; Ideal 3,457.54.
- Good trap question: Ideal is the best cut but has the lowest average price. Why? Average carat by cut: Fair 1.046, Premium 0.892, Good 0.849, Very Good 0.806, Ideal 0.703. Ideal stones are smaller on average, and a plain average does not hold carat constant. [measured; the explanation is synthesis]
- The JOIN question uses a tiny 2-table example: `predictions(id, predicted_price)` and `actuals(id, price)`, 3 rows each, invented for the question [fictional]. It previews Week 12, where predictions meet real prices.

**Limits and common mistakes.**
- `table` is a column name and a SQL keyword. Quote it as `"table"`. [measured: needed in our `CREATE TABLE`]
- The self-check is not graded and blocks nothing. [source: CURRICULUM line 251]

**Diagram spec.** None.

**Demo and practical link.** Self-paced. The final 8 questions, options and answer key are written in M00-SELF-PACED from the numbers above.

**Sources.** CURRICULUM line 251 (read-part). `Planned_Syllabus_Additions.md` lines 46 to 50 and 61 to 64 (read during P-10 map build). SQLBolt (doc-verified 2026-10-05, notes A #22). Measured results (notes Part C and this run).

---

## Topic 12. macOS and native Linux differences

**Objective.** A student on a Mac or on native Ubuntu can reach the same 3 passing checks. (Objective 1: "or the native terminal on macOS/Linux".)

**Status.** Doc-checked on 2026-10-07. **Not tested on a Mac.** The deck and practical must mark the macOS steps as untested until someone runs them on a Mac. [decision]

**Native Ubuntu.** Ubuntu 24.04 LTS only. Same commands as WSL Ubuntu. Skip Topics 2 and 3's WSL steps. For Docker, install Docker Engine and do the `docker` group step from Topic 7. [source: notes A #8]

**macOS.**
- Terminal: the built-in Terminal app. Skip WSL. VS Code opens folders directly; no WSL extension. [synthesis]
- Python 3.12: python.org's last 3.12 release with a macOS installer is 3.12.10 (April 8, 2025), "macOS 64-bit universal2 installer". 3.12.11 and later are source-only security releases with "No installers". Use the 3.12.10 universal2 installer, then `python3.12 -m venv .venv` as in Topic 5. [source: python.org "Python Releases for macOS" and release pages, doc-verified 2026-10-11]
- Locked packages: `requirements.txt` is locked for Python 3.12 on Linux and macOS. [source: `m00` README lines 29 to 31]
- Docker: Docker Desktop for Mac, the "Mac with Apple silicon" or "Mac with Intel chip" installer. [source: docs.docker.com/desktop/setup/install/mac-install/, doc-verified 2026-10-07]
- AWS CLI: `curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"`, then `sudo installer -pkg AWSCLIV2.pkg -target /`. No `unzip` step. [source: AWS CLI install page, macOS section, doc-verified 2026-10-07]
- Git and SSH key: same `git config` and `ssh-keygen` commands; use the macOS tab of the GitHub page. [source: notes A #20, Linux tab checked; macOS tab not read, so the practical must check it]
- The verify script is bash and runs on macOS unchanged. [synthesis: `verify_setup.sh` uses only bash, `command -v`, `aws`, `docker` and the venv Python. Not run on a Mac]

**Limits.** Untested. If the practical cannot get a Mac test before Nov 7, Daniel decides whether macOS stays supported for the pilot (Open items).

**Sources.** As cited above.

---

## Not in Week 0 (scoped out on purpose)

- **Minikube.** Psitron and `module-readmes/00-README.md` install it in Week 0. CURRICULUM puts it in Week 8. Install it there and keep Week 0 at about 3 hours. [decision: source-map "Not in M00" and conflict 4]
- **GCP and Azure accounts.** AWS only. [source: PROJECT_STATE Decisions 2026-07-03]
- **Jupyter as a separate install.** `jupyterlab` 4.6.4 is in the locked `requirements.txt`. [source: `requirements.in` at `m00`]
- **`aws login`, IAM Identity Center, the AWS MCP server, Agent Toolkit for AWS.** Named once in Topic 8 as what real teams use or as prompts to decline. Not installed. [decision]
- **Psitron Day 1 0:00 to 1:43:08 "Prerequisites validation".** No transcript; Windows-native and three clouds. Not used. [source: videos.md]

## How the topics fit Week 0

**Self-paced (about 3 hours)** [decision, estimate; Daniel times it on a clean WSL install during his prep]:

| Order | Piece | Topics | Estimate |
|---|---|---|---|
| 1 | Setup guide part 1: WSL2, Ubuntu, VS Code | 2, 3 | 30 min, plus restarts |
| 2 | Bash lesson | 4 | 60 min |
| 3 | Setup guide part 2: Python 3.12, venv, Git and SSH, Docker | 5, 6, 7 | 40 min |
| 4 | Setup guide part 3: AWS account and CLI | 8 | 30 min, plus waiting for the activation email (minutes, up to 24 hours) |
| 5 | Run the verify script | 9 | 10 min |
| 6 | SQL self-check | 11 | 10 min |

Setup video (about 20 min, Daniel's screen recording) follows the same order as the setup guide.

**Live session (90 minutes)**, from CURRICULUM line 254:

| Time | Topics |
|---|---|
| 0:00 to 0:15 | Topic 1 (welcome, course map, how a week works, grading). One slide of Topic 10 (how to ask for help) |
| 0:15 to 1:20 | Breakouts: WSL (Topics 2, 3), Docker (Topic 7), AWS (Topic 8). Use the Topic 10 question format |
| 1:20 to 1:30 | Everyone runs `bash scripts/verify_setup.sh` (Topic 9) |

## Slide candidates (not a deck design)

CURRICULUM plans about 15 slides. The old deck had 24. Indispensable messages and figures:
1. Where we are: course map with Week 0 lit (Topic 1).
2. How a week works, and Week 0 is pass/fail (Topic 1).
3. Grading and AI policy (Topic 1).
4. Works on my machine, so one standard environment (Topic 2).
5. Where does my code run? WSL2 diagram, with "keep files in `~`" and the 15 minutes vs under 1 minute result (Topics 2, 3).
6. Python 3.12, one venv per project, locked with hashes (Topic 5).
7. Bash cheat sheet: the 5 blocks on one slide (Topic 4).
8. The pipe diagram on diamonds (Topic 4).
9. Three layers of AWS access, with "Never create root access keys" in bold (Topic 8).
10. The alert comes after the spend, so delete the same day (Topic 8).
11. What real teams use instead of IAM user keys (Topic 8, one line).
12. Three checks, one green line (Topic 9).
13. Top 5 failures and fixes: virtualization off, files in `/mnt/c`, missing `unzip` or `python3.12`, Docker not running, root keys (Topics 2, 5, 7, 8).
14. How to ask for help (Topic 10).
15. Run it now (Topic 9).

Speaker notes only: why Week 0 exists (dropout); Psitron's WSL detour story; the Docker license numbers; the Agent Toolkit prompt; the two AWS sign-up paths in detail.

Deeper reading: MIT Missing Semester lecture 1 (required for the Bash lesson). Optional: cmdchallenge.com, SQLBolt, Microsoft "Working across file systems".

## Open items for Daniel (none block G4)

1. **"Billing alarm" becomes "budget alert".** This PR now edits CURRICULUM.md (Week 0 objective 4, Week 0 Concepts, Week 10 cost line). Only you can merge it. Your merge settles the wording.
2. **Payment card and SMS check** come from one test account. Re-check on one more fresh account before Nov 7.
3. **Python 3.12 install** passes on Ubuntu 24.04.5 LTS (Topic 5, measured 2026-10-11). It is still untested on a fresh `Ubuntu-24.04` WSL install. Daniel's timed setup (instructor notes section 0) runs it there.
5. **macOS** is in CURRICULUM objective 1 but untested (Topic 12). Recommendation: keep it, and test on one Mac before Nov 7. If no Mac is available, say "macOS: best effort" in the student guide.
4. **Student repo URL**: `https://github.com/dislam7991/innovatics-mlops-course` (P-19, pushed 2026-10-25). Topic 6 names it.
