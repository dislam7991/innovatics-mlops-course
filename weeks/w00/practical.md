---
module: m00
title: "Practical 0: Set up your machine"
solution_tag: m00
start_branch: start-m00
grading: pass/fail (does not count toward the final grade; must pass before Week 1)
time: about 3 hours, self-paced, before the Week 0 live session
source: modules/m00-onboarding/content.md (merged PR #39 at 1ab1676)
---

# Practical 0: Set up your machine

## Goal

Get one working environment that you will use for all 14 weeks: Linux, VS Code, Python 3.12, Git, Docker, and a safe AWS account. At the end you run one script that proves it all works.

**Evidence:** `bash scripts/verify_setup.sh` passes all 3 checks from a clean clone of the starter repo.

**Time:** about 3 hours. Much of it is waiting for downloads, restarts and the AWS activation email. Start early in the week, so the live session can fix anything that is left.

| Order | Part | Steps | Time |
|---|---|---|---|
| 1 | Linux and VS Code | 1, 2 | 30 min, plus restarts |
| 2 | Bash lesson (separate file: `bash-lesson.md`) | | 60 min |
| 3 | Tools: Python 3.12, Git and GitHub, Docker | 3, 4, 5 | 40 min |
| 4 | AWS account and CLI | 6 | 30 min, plus the activation email (minutes, up to 24 hours) |
| 5 | Clone, install, verify | 7, 8, 9 | 15 min |
| 6 | SQL self-check (separate file: `sql-self-check.md`) | | 10 min |

## What you need before you start

- A laptop you can install software on. On a work laptop you may need IT to give you admin rights. Tell the instructor early if you cannot get them.
- 8 GB of RAM or more and about 20 GB of free disk space.
- An email address for GitHub and one for AWS (they can be the same).
- A payment card may be needed. On our test account (October 2026) AWS asked for a card and said it would hold $1. You may or may not be asked.
- One of these setups:

| Your computer | Status | Follow |
|---|---|---|
| Windows 10 (version 2004 or later) or Windows 11 | Tested. Every command in this course runs inside Ubuntu in WSL2 | Steps 1 to 9 |
| Ubuntu Linux 24.04 LTS | Same commands as WSL Ubuntu. Ubuntu 22.04 ships Python 3.10 and is not supported | Skip Steps 1 and 2's WSL parts. Use the Linux path in Step 5 |
| macOS | Documented, **not yet tested on a Mac**. Best effort | The "macOS" boxes in Steps 3 and 6. Tell the instructor you use a Mac |

Native Windows (PowerShell or Command Prompt for course work) is not supported. On Windows, the only commands you type outside Ubuntu are in Step 1.

## How to read this guide

- Operating system setup changes with each vendor release. For the long installs, this guide links to the **official page** and names the section to follow. Do not follow random blog posts: versions matter.
- Commands from the course repo name their file and line at tag `m00`. Every other command is a one-time setup command copied from the official page linked in the same step. Those pages are the source of truth when a vendor changes its installer.
- Facts that change often (versions, credits, prices) say when we checked them.

---

## Step 1. Install WSL2 and Ubuntu (Windows only)

WSL2 (Windows Subsystem for Linux, version 2) runs a real Ubuntu inside Windows. MLOps tools assume Linux, so the whole class works in the same Linux setup.

1. Open **PowerShell** with **Run as administrator** (right-click, "Run as administrator"). Command Prompt as administrator also works.
2. Type this and press Enter:
   ```
   wsl --install -d Ubuntu-24.04
   ```
   It installs WSL and Ubuntu 24.04 LTS. Microsoft's page: [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

   **Type the `-d Ubuntu-24.04` part.** A plain `wsl --install` now gives Ubuntu 26.04, which ships Python 3.14. The course's locked packages need Python 3.12, and Ubuntu 24.04 ships 3.12 (checked October 2026).
3. Restart your computer when it asks.
4. After the restart an Ubuntu window opens. Choose a Linux user name and password. Write the password down: every `sudo` command asks for it. The password prompt shows no characters while you type. That is normal.
5. If the install hangs at 0.0%, run this instead, in the same administrator window:
   ```
   wsl --install --web-download -d Ubuntu-24.04
   ```

**Done with this step when:** you can open **Ubuntu 24.04** from the Start menu and type in its terminal.

> **Error 0x80370102 or 0x80070003?** Virtualization is off. See the first row of Troubleshooting.

### Where to keep your files

Ubuntu has its own disk. Your Linux home folder is `/home/<your-linux-user>`, written `~`. Your Windows C: drive appears as `/mnt/c`.

**Keep all course work under `~`.** Do not work under `/mnt/c/...`. In our test, the package install in Step 8 ran for over 15 minutes under `/mnt/c` and looked frozen. The same install in `~` took under 1 minute.

Check it now. In Ubuntu, type:

```
cd ~
pwd
```

You should see `/home/<your-linux-user>`.

## Step 2. Install VS Code and connect it to WSL (Windows only)

1. Install [VS Code](https://code.visualstudio.com/) on **Windows**. In the installer, keep **Add to PATH** checked. Then `code .` works from Ubuntu.
2. In VS Code, install the **WSL** extension (id `ms-vscode-remote.remote-wsl`). Older guides call it "Remote - WSL". It is the same tool. Microsoft's page: [Developing in WSL](https://code.visualstudio.com/docs/remote/wsl).
3. In the Ubuntu terminal, type `code .`. VS Code opens, connected to Ubuntu.
4. Check the bottom-left corner of VS Code. It shows that you are connected to WSL (for example **WSL: Ubuntu-24.04**).
5. Open a terminal in VS Code (**Terminal > New Terminal**) and type `pwd`. It prints a `/home/...` path.

**Always open course folders from Ubuntu** (`code .`) or with the command **WSL: Reopen Folder in WSL**. If you open them from Windows Explorer, VS Code runs on the Windows side, and the terminal and Python are wrong.

macOS and Linux: install VS Code and open folders directly. You do not need the WSL extension.

**Done with this step when:** on Windows, VS Code shows the WSL indicator in the bottom-left corner, and its terminal prints a `/home/...` path. On Ubuntu or macOS, `code .` opens VS Code, and its terminal prints your home folder path (`/home/...` on Ubuntu, `/Users/...` on macOS).

**Now do the Bash lesson** (`bash-lesson.md`, 60 minutes). The rest of this guide assumes you can use `cd`, `ls` and `sudo`.

## Step 3. Install base tools and Python 3.12

The diamond project needs **Python 3.12** exactly. The locked packages are built for 3.12, and the notebook check refuses any other version. Ubuntu 24.04 ships Python 3.12 as its system Python (3.12.3, checked October 2026), so you need no extra package source.

**Do not remove or replace the system `python3`.** Ubuntu's own tools depend on it. On Ubuntu 24.04 it is also the course Python.

In the Ubuntu terminal:

```
sudo apt update
sudo apt install -y git curl unzip make python3-venv
python3.12 --version
```

You should see `Python 3.12.3` (when we checked, October 2026).

- `unzip` is needed for the AWS CLI in Step 6. Fresh Ubuntu may not have it.
- `make` runs the course commands from Week 2 on (`make install`, `make test`). The Ubuntu 24.04 WSL image does not include it (checked October 2026).
- `python3-venv` adds the `venv` module. Without it, Step 8 fails with `The virtual environment was not created successfully because ensurepip is not available.`

> **macOS (untested).** Install Python 3.12.10 from python.org, using the "macOS 64-bit universal2 installer". It is the last 3.12 release with a macOS installer; later 3.12 releases are source-only security releases with no installers (checked October 2026). Install Git with `xcode-select --install` or from [git-scm.com](https://git-scm.com/). Check with `python3.12 --version`.

**Done with this step when:** `git --version`, `make --version` and `python3.12 --version` all print a version.

## Step 4. Set up Git and GitHub

GitHub needs proof that pushes come from you. The course uses an **SSH key**: a key pair. The private key stays on your laptop. The public key (the `.pub` file) goes to GitHub.

1. Create a free account at [github.com](https://github.com/) if you do not have one.
2. Tell Git who you are. Use your own name and your GitHub email:
   ```
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```
3. Create the key **inside Ubuntu** (not on the Windows side). Accept the default file name. Follow GitHub's [Generating a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), **Linux** tab (macOS users: the macOS tab):
   ```
   ssh-keygen -t ed25519 -C "you@example.com"
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```
4. Print the **public** key with `cat ~/.ssh/id_ed25519.pub`. Copy it into GitHub with [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
5. Test it:
   ```
   ssh -T git@github.com
   ```
   The first time, type `yes` to trust GitHub's host. You should see `Hi <your-user>! You've successfully authenticated...`.

Never share or paste the file without `.pub`. That is your private key.

**Done with this step when:** `ssh -T git@github.com` greets you by your GitHub user name.

## Step 5. Install Docker

Docker runs software in containers: a program packaged with everything it needs. We use it from Week 7. Week 0 only checks that it works.

- **Windows:** follow [Install Docker Desktop on Windows](https://docs.docker.com/desktop/setup/install/windows-install/), section **Install interactively**. Use the **WSL 2** backend. Docker Desktop needs WSL version 2.1.5 or later. If Docker or the docker CLI was installed inside Ubuntu before, uninstall it first. Then open Docker Desktop **Settings > Resources > WSL Integration** and check that **Ubuntu-24.04** is on. Close and reopen your Ubuntu window. Docker's page: [Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/features/wsl/).
- **Ubuntu (native Linux):** follow [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/), section **Install using the apt repository**. Then follow [Linux post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/), **Manage Docker as a non-root user**: add yourself to the `docker` group, then log out and back in (or run `newgrp docker`). Note: the `docker` group gives root-level power on that machine.
- **macOS (untested):** follow [Install Docker Desktop on Mac](https://docs.docker.com/desktop/setup/install/mac-install/). Pick "Mac with Apple silicon" or "Mac with Intel chip". Start Docker Desktop once.

> **Licensing.** Docker Desktop is free for personal use, education, non-commercial open source, and businesses with fewer than 250 employees **and** less than 10 million USD a year in revenue (checked October 2026). On a work laptop at a larger company, check with your employer first.

**Check it.** Start Docker Desktop (Windows and macOS). Then, in Ubuntu or your terminal, run the same pinned image the verify script uses. This command is copied from `diamond-mlops/scripts/verify_setup.sh` at tag `m00`, line 27:

```bash
docker run --rm hello-world@sha256:ec153840d1e635ac434fab5e377081f17e0e15afab27beb3f726c3265039cfff
```

You should see `Hello from Docker!`. The `@sha256:` value pins one exact image, the same idea as the locked Python packages. `--rm` deletes the container when it exits.

**Done with this step when:** you see `Hello from Docker!`.

## Step 6. Set up a safe AWS account

You deploy to AWS in Weeks 7 to 10. The account must be safe before then. **Read this whole step before you start.**

> **Never create access keys for the AWS root user.** The root user is the email and password you sign up with. It can do anything, including close the account. A leaked root key gives a stranger full control.

### 6a. Sign up

1. Go to [aws.amazon.com](https://aws.amazon.com/) and start the sign-up.
2. AWS may show a choice between two sign-up paths. Choose **"Sign up for AWS (advanced)"**. It creates the classic account this course is built on: a root user, any Region, and IAM users with access keys. The other path ("Sign up for AWS (new)") is not supported in this course.
3. Follow only **Step 1** of AWS's sign-up page. Skip its Step 2 (`aws login`) and Step 3 (AWS MCP Server). The verify script rejects a root login on purpose, and the MCP server is not used in this course.
4. Choose the **Free plan**.
5. Wait for the activation email. It can take minutes, or up to 24 hours.

**What the Free plan gives you** (checked October 2026; AWS changes this, so read the [Free Tier page](https://aws.amazon.com/free/) when you sign up):
- New accounts get $100 in credits, plus up to $100 more for completing set activities.
- The Free plan ends after 6 months **or** when the credits are used up, whichever comes first. AWS then suspends the account and keeps its content for 90 days. Upgrading to the Paid plan within those 90 days restores access.
- The course runs about 4 months. **The account lasts the course if you do not use up the credits.** Delete what you create the same day, and check your credit balance in the Billing console each week.

### 6b. Protect the root user

1. Sign in as the root user.
2. Open the account menu (top right) > **Security credentials**. Turn on **multi-factor authentication (MFA)**. An authenticator app on your phone is fine. AWS requires root MFA within 35 days of first sign-in anyway.
3. Do **not** create access keys on this page.

### 6c. Create a budget alert

1. In the console search bar, open **Billing and Cost Management > Budgets > Create budget**.
2. Choose **Use a template (simplified)**, then **Monthly cost budget**. AWS's guide: [Using a budget template](https://docs.aws.amazon.com/cost-management/latest/userguide/budget-templates.html).
3. Set the amount to **$5** and enter your email. Click **Create budget**.
4. Optional: also create a **Zero spend budget**. It emails you when spending goes over the Free Tier limits.

What a budget does, and what it does not do:
- It **emails you** when spending passes, or is forecast to pass, the amount.
- It **does not stop anything.** Budget data updates up to 3 times a day, typically 8 to 12 hours apart. The email can arrive after the money is spent.
- The real protection is a habit: **delete what you create the same day.** Every cloud practical in this course ends with a cleanup step.

### 6d. Create your course IAM user

1. Open **IAM > Users > Create user**.
2. User name: `mlops-student`. Leave **console access** off. You use this user from the command line only.
3. On the permissions page, **attach no policy**. Click **Next**, then **Create user**.

Why no permissions: check 1 only asks AWS "who am I?" (`sts get-caller-identity`). AWS documents that this call needs no permissions. Later weeks add only the permissions that week needs. That is **least privilege**: if this key ever leaks, it can do almost nothing.

Real teams usually give people short-term credentials (IAM Identity Center or `aws login`) instead of long-term IAM user keys. We use one IAM user because it is simpler for a personal learning account. Do not copy this pattern into a company.

### 6e. Create an access key

1. Open **IAM > Users > mlops-student > Security credentials > Create access key**.
2. Use case: **Command Line Interface (CLI)**. AWS shows alternatives to long-term keys. For this course, an IAM user key is what we use. Tick the confirmation box, click **Next**, then **Create access key**.
3. Keep the page open. You see the secret key **only once**.

### 6f. Install and configure the AWS CLI

In Ubuntu. These are the commands from AWS's [Install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) page, Linux x86 (64-bit):

```
cd ~
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

You should see `aws-cli/2.x.x`. You can then delete `awscliv2.zip` and the `aws` folder. On an ARM laptop (`uname -m` prints `aarch64`), use the **Linux ARM** installer from the same page.

> **macOS (untested).** `curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"`, then `sudo installer -pkg AWSCLIV2.pkg -target /`. No `unzip` step.

Now configure it:

```
aws configure
```

It asks 4 questions:

| Question | Answer |
|---|---|
| AWS Access Key ID | The key ID from 6e |
| AWS Secret Access Key | The secret from 6e |
| Default region name | `us-east-1` |
| Default output format | `json` |

- The keys are saved in `~/.aws/credentials`, in your Linux home folder, outside every project.
- Newer CLI versions may then ask whether to install the "Agent Toolkit for AWS" (AWS skills and an MCP server for AI coding agents). The course does not use it. Answer `n`, or `never` to stop the question for good.
- Close the AWS key page. Never put keys in a project folder, a chat, an email or Git.

**Check it:** `aws sts get-caller-identity`. The `Arn` must end in `:user/mlops-student`. If it ends in `:root`, you configured root keys: delete them now (see Troubleshooting). **Do not share this output.** It shows your account ID. Step 9 checks it for you and prints only PASS or FAIL.

**If a key ever leaks** (pushed to GitHub, pasted in a chat, in a screenshot): in IAM, **deactivate** the key, create a new one, run `aws configure` again, then delete the old key.

**Done with this step when:** root has MFA and no access keys, the $5 budget exists, and `aws sts get-caller-identity` shows `:user/mlops-student`.

## Step 7. Get the starter repo

The course repo is `https://github.com/dislam7991/innovatics-mlops-course`. First make your own copy of it. Open that page in your browser, select **Fork**, keep the name, and keep the fork **public**. A public fork gets free GitHub Actions minutes, which Week 2 needs.

Then clone your fork, not the course repo. Replace `<your-user>` with your GitHub user name:

```
cd ~
git clone git@github.com:<your-user>/innovatics-mlops-course.git
```

Enter the folder and add the course repo as `upstream` (each week you fetch the new starter from it). Your fork's `main` is the Week 0 starting point, so you stay on it:

```
cd innovatics-mlops-course
git remote add upstream https://github.com/dislam7991/innovatics-mlops-course.git
git remote -v
cd diamond-mlops
```

`git remote -v` must list `origin` (your fork) and `upstream` (the course repo), each twice. From now on, every command in this practical runs inside `diamond-mlops`. Type `pwd`: the path must start with `/home/`, not `/mnt/c`.

## Step 8. Install the notebook environment

Each project gets its own **virtual environment** (`.venv`): a folder with its own Python packages, so projects do not break each other. It never goes into Git (`.gitignore` lists `.venv/`). You can delete it and rebuild it any time.

This block is copied from `diamond-mlops/README.md` at tag `m00`, lines 16 to 19. Line 15 (`cd diamond-mlops`) is left out because you are already there:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -m jupyterlab
```

- `--require-hashes` installs only the exact locked files. If any file does not match its hash, the install stops. No silent upgrades. This matters: a newer scikit-learn moves the notebook's MAE from 279.29 to 278.16.
- The install can be quiet for a long time. Our test took about 1 minute in `~` (73 seconds for the install with `--no-cache-dir` and `pip check`, Ubuntu 24.04, October 2026). To see progress, open a second terminal and run `du -sh .venv` twice, 30 seconds apart. If the number grows, it is working.
- `pip check` should print `No broken requirements found.`
- JupyterLab prints a link. Open it in your browser, open `notebooks/01_diamond_exploration.ipynb`, choose the Python 3 kernel, and run all cells. Look through the results. Then stop JupyterLab with `Ctrl+C` in the terminal.

**Do not** `pip install` anything else into this `.venv`. Keep XGBoost out: the notebook picks it up if it is installed, and the winning model changes.

Optional disk-space tip: adding `--no-cache-dir` to the install line skips a second copy of every package in `~/.cache/pip`. The environment and cache came to about 650 MB on our test machine.

## Step 9. Run the verification script

From the `diamond-mlops` folder. This command is copied from `diamond-mlops/README.md` at tag `m00`, line 43:

```bash
bash scripts/verify_setup.sh
```

Use `bash scripts/...`. Typing `./scripts/verify_setup.sh` gives `Permission denied`, because the file is not marked executable.

First the script checks that `.venv` exists. If it does not, it stops at once with `FAIL: create the Python 3.12 .venv and install requirements.txt first.` and runs no checks. Once `.venv` exists, it runs all 3 checks, even if one fails, and then reports:

1. **AWS:** `aws sts get-caller-identity` must return an IAM user. Root and role identities fail on purpose. It creates nothing in AWS.
2. **Docker:** runs the pinned `hello-world` image and removes the container.
3. **Notebook:** runs every cell of the diamond notebook in your `.venv` and compares MAE, RMSE and R2 with the reference numbers. It also checks the model is HistGradientBoosting with seed 42 and 10,755 holdout rows. This takes from under a minute to several minutes, depending on your laptop.

A passing run ends like this. These lines are printed by `scripts/run_notebook.py` and `scripts/verify_setup.sh` at tag `m00`:

```text
MAE: 279.292629032577
RMSE: 524.9243546483148
R2: 0.982563973914643
PASS notebook: every cell executed; diamond metrics match (absolute tolerance 1e-9).
Setup ready: all 3 checks passed.
```

You may also see `Kernel is running over TCP without encryption`. That warning is expected. Only the `PASS` and `FAIL` lines matter.

If a check fails, the script ends with `Setup incomplete: N of 3 checks failed.` Read the `FAIL` line. It says what to do next. Fix it with the Troubleshooting table and run the script again.

---

## What to submit

Post in the course help channel, or upload where your instructor asks:

1. The end of the `verify_setup.sh` output, from the `MAE:` line to the last line, **as text**. It must end with `Setup ready: all 3 checks passed.`
2. Your setup, for example "Windows 11, Ubuntu 24.04 in WSL2" or "macOS 15".

**Do not** post the output of `aws sts get-caller-identity` or anything from `~/.aws/`. The script prints only PASS or FAIL for AWS, so its output is safe to share.

## Done when

- [ ] `bash scripts/verify_setup.sh` ends with `Setup ready: all 3 checks passed.`
- [ ] You ran it from a clean clone of the starter repo, under `~`, with a `.venv` made by Python 3.12.
- [ ] The AWS check passed as the IAM user `mlops-student`, not root.
- [ ] Your AWS root user has MFA on and **no** access keys.
- [ ] You have a $5 monthly cost budget with an email alert.
- [ ] `ssh -T git@github.com` greets you by your GitHub user name.

## Rubric (pass/fail)

Week 0 does not count toward the final grade. You must pass it before the Week 1 session.

| Result | Meaning |
|---|---|
| **Pass** | The submitted output contains the `PASS notebook` line and ends with `Setup ready: all 3 checks passed.` The script itself compares the metrics with the reference numbers |
| **Not yet** | A check fails, or the output is missing. Fix it and resubmit. You can resubmit as many times as you need before Week 1 |

The last 3 items in **Done when** (root MFA, budget, SSH) are self-checks. The instructor may ask you to show them on screen during the live session.

## Troubleshooting

When you ask for help, give the command you ran, the full error **as text**, what you already tried, and your setup. Screenshots of text cannot be searched. Never paste keys or passwords.

| You see | Cause | Fix |
|---|---|---|
| `wsl --install` fails with `0x80370102` or `0x80070003` | Virtualization is off | Turn on the Windows feature **Virtual Machine Platform**. Restart into your BIOS or UEFI settings and turn on virtualization (Intel VT-x or AMD SVM). The menu name depends on your laptop maker |
| `wsl --install` asks for rights or fails at once | The terminal is not an administrator terminal | Close it. Right-click PowerShell, choose **Run as administrator**, and run it again |
| `wsl --install` hangs at 0.0% | Download problem | `wsl --install --web-download -d Ubuntu-24.04` |
| Install or `git` is very slow, or `$'\r': command not found` | The project is under `/mnt/c/` | `cd ~` and clone again there |
| VS Code terminal shows a Windows path, or no WSL indicator | The folder was opened from Windows | In Ubuntu: `cd` to the folder, then `code .` |
| `unzip: command not found` | Fresh Ubuntu has no `unzip` | `sudo apt update`, then `sudo apt install -y unzip` |
| `make: command not found` | Fresh Ubuntu has no `make` | `sudo apt update`, then `sudo apt install -y make` |
| `python3.12: command not found` | Ubuntu is not 24.04 (for example 26.04 from a plain `wsl --install`, or 22.04) | Run `lsb_release -d`. It must show Ubuntu 24.04. On Windows, install it with `wsl --install -d Ubuntu-24.04` (Step 1) and work in that distribution |
| `The virtual environment was not created successfully because ensurepip is not available.` | `python3-venv` is missing | `sudo apt install -y python3-venv`, then `rm -rf .venv` and create it again |
| `FAIL: create the Python 3.12 .venv and install requirements.txt first.` | Step 8 was skipped, or the script ran from the wrong folder | `cd` into `diamond-mlops` and do Step 8 |
| `THESE PACKAGES DO NOT MATCH THE HASHES` | A download was corrupted or changed | Run the install again. If it repeats, `rm -rf .venv` and redo Step 8 |
| `./scripts/verify_setup.sh: Permission denied` | The file is not executable | Type `bash scripts/verify_setup.sh` |
| `docker: command not found` in Ubuntu | WSL integration is off | Docker Desktop > Settings > Resources > WSL Integration > turn on Ubuntu-24.04 > Apply & restart. Reopen Ubuntu |
| `Cannot connect to the Docker daemon` or `failed to connect to the docker API` | Docker is not running | Start Docker Desktop and wait until it is running. Native Linux: `sudo systemctl start docker` |
| `permission denied ... /var/run/docker.sock` (native Linux) | Your user is not in the `docker` group | Docker's post-install steps, then log out and back in |
| `FAIL AWS: install AWS CLI v2 and configure your student IAM user credentials.` | `aws` is missing, has no credentials, or cannot reach AWS | Run `aws --version`, then `aws configure`, then `aws sts get-caller-identity` and read its error |
| `FAIL AWS identity: Week 0 requires an IAM user; root and role identities fail.`, ARN ends in `:root` | You configured root keys | Sign in as root, open **Security credentials**, **delete** the root access key. Create a key for `mlops-student` (6e) and run `aws configure` again |
| Same message, ARN contains `assumed-role` | You used IAM Identity Center (SSO) or a role | Week 0 needs an IAM user key. Do 6d and 6e. If you set `AWS_PROFILE`, point it at the IAM user profile |
| `InvalidClientTokenId` or `SignatureDoesNotMatch` | Key ID or secret pasted wrong | Run `aws configure` again. If the secret is lost, create a new key and deactivate the old one |
| `Could not connect to the endpoint URL` | No network, or a typo in the region | Check your internet, and that the region is `us-east-1` |
| Notebook metrics differ from the reference numbers | Packages differ from the lock (newer scikit-learn, or XGBoost installed) | `rm -rf .venv` and redo Step 8 exactly |
| Notebook check is killed or times out | Not enough memory | Close other apps, especially browsers, and run it again |
| Work laptop blocks installs | No admin rights | Ask IT for admin rights, or use a personal laptop. Tell the instructor before the live session |

## Before Week 1

- Finish the Bash lesson (`bash-lesson.md`). Every lab uses the terminal.
- Take the 10-minute SQL self-check (`sql-self-check.md`).
- Keep your setup. Do not delete `.venv` or `~/.aws/`. Every later week uses this environment.
