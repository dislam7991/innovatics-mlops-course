---
module: m00
title: "Bash basics (60 minutes, self-paced)"
tag: m00
grading: not graded
source: modules/m00-onboarding/content.md Topic 4 (merged PR #39 at 1ab1676)
---

# Bash basics

Every lab in this course uses the terminal. This lesson gives you the commands you need, in 5 short blocks, then 10 exercises on the diamond project.

**Before you start:** finish Steps 1 and 2 of Practical 0 (WSL2, Ubuntu, VS Code). Open the Ubuntu terminal, or the terminal inside VS Code.

**Deeper reading** (optional now, about 45 minutes; read it before Week 2): [MIT Missing Semester, lecture 1: The Shell](https://missing.csail.mit.edu/2020/course-shell/).

**Optional practice:** [cmdchallenge.com](https://cmdchallenge.com/) (one-line shell challenges in the browser).

| Block | Topic | Time |
|---|---|---|
| 1 | Where am I, what is here | 8 min |
| 2 | Make, copy, move, delete | 8 min |
| 3 | Look inside files | 8 min |
| 4 | Connect commands | 10 min |
| 5 | Environment variables and scripts | 10 min |
| | Exercises on the diamond project | 16 min |

Type every command yourself. Do not paste. Typing is how your hands learn it.

---

## Block 1. Where am I, what is here

| Command | What it does |
|---|---|
| `pwd` | Print the folder you are in ("print working directory") |
| `ls` | List the files in this folder |
| `ls -la` | List all files, including hidden ones (names that start with `.`, such as `.gitignore`), with details |
| `cd folder` | Go into `folder` |
| `cd ..` | Go up one folder |
| `cd ~` | Go to your home folder (`/home/<you>`) |
| `cd -` | Go back to the folder you were in before |

Try it:

```
cd ~
pwd
mkdir -p practice
cd practice
pwd
cd ..
pwd
```

Tip: press **Tab** to complete a file or folder name. Press it twice to see the choices.

## Block 2. Make, copy, move, delete

| Command | What it does |
|---|---|
| `mkdir -p a/b` | Make folder `a` and folder `b` inside it. `-p` makes the parents too, and is quiet if they exist |
| `cp file copy` | Copy a file |
| `mv old new` | Move a file. Moving to a new name in the same folder renames it |
| `rm file` | Delete a file |
| `rm -r folder` | Delete a folder and everything in it |

> **Warning.** `rm` has no recycle bin and no undo. `rm -r` deletes everything inside the folder. Read the command twice before you press Enter.

Try it:

```
cd ~/practice
echo "hello" > note.txt
cp note.txt note2.txt
mv note2.txt renamed.txt
ls
rm renamed.txt
ls
```

## Block 3. Look inside files

| Command | What it does |
|---|---|
| `cat file` | Print the whole file |
| `less file` | Scroll through a file. Arrow keys move, `/word` searches, `q` quits |
| `head -3 file` | Print the first 3 lines |
| `tail -5 file` | Print the last 5 lines |
| `tail -f file` | Keep printing new lines as a file grows (useful for logs). `Ctrl+C` stops it |

## Block 4. Connect commands

| Symbol or command | What it does |
|---|---|
| `a \| b` | The **pipe**. The output of `a` becomes the input of `b` |
| `a > file` | Write the output of `a` to `file`. **Replaces** the file if it exists |
| `a >> file` | **Adds** the output of `a` to the end of `file` |
| `grep text file` | Print the lines that contain `text` |
| `grep -c text file` | Count the matching lines |
| `grep -i text file` | Ignore upper and lower case |
| `grep -n text file` | Show line numbers |
| `wc -l file` | Count lines |

Read a pipe from left to right. Each command does one small job.

> **Warning.** `>` replaces a file with no question. Use `>>` when you want to add.

## Block 5. Environment variables and scripts

| Command | What it does |
|---|---|
| `export NAME=value` | Set an environment variable for this terminal and the programs it starts |
| `echo $NAME` | Print the variable's value |
| `echo $PATH` | `PATH` is the list of folders the shell searches for commands |
| `which python3.12` | Show which file runs when you type `python3.12` |
| `chmod +x file` | Make a file executable |
| `./script.sh` | Run an executable file in this folder |
| `bash script.sh` | Run a bash script, executable or not |
| `history` | List your past commands. `Ctrl+R` searches them |
| `sudo command` | Run one command as the administrator (root). It asks your Linux password, and shows no characters while you type |

**Exit codes.** Every command returns a number when it ends. `0` means success. Any other number means failure. Scripts and CI pipelines use this number to decide what happens next. Print the last one with `echo $?`.

Try it:

```
export COURSE=mlops
echo $COURSE
which python3.12
ls /no/such/folder
echo $?
```

The last line prints a number that is not `0`, because `ls` failed.

`export` works only in the terminal where you typed it. A new terminal does not know `COURSE`. To keep a setting, add the `export` line to `~/.bashrc`, then run `source ~/.bashrc`.

---

## Exercises on the diamond project

Do these after Step 7 of Practical 0 (clone the starter repo), or come back to them. Run them inside `diamond-mlops/`:

```
cd ~/<your-course-repo>/diamond-mlops
```

Write your answer down, then check it in the answers section at the end.

1. Show the first 3 lines of `data/raw/diamonds.csv`. What are the column names? What is the price of the first diamond?
2. How many lines does `data/raw/diamonds.csv` have? How many diamonds is that?
3. How many lines contain `,Ideal,`?
4. Write only the `Ideal` lines to a new file `~/practice/ideal.csv` with `>`. Count its lines.
5. Run your command from exercise 4 again, but with `>>`. Count the lines again. Why did the number change?
6. Show the hidden files in `diamond-mlops/`. What does `cat .gitignore` show? Find `.venv/` and `.env` in it.
7. Run `ls -l scripts`. Is there an `x` in the permissions of `verify_setup.sh`? Try `./scripts/verify_setup.sh`, then `echo $?`. What happened, and what number did you get?
8. Set `export GREETING=hello`. Open a second terminal and run `echo $GREETING`. What do you see, and why?
9. Read `scripts/verify_setup.sh` with `less`. Find: the line that checks if `aws` is installed; the pipe from `aws sts ...` into Python; the line that counts failures; the line that tells the caller the script failed.
10. **Stretch.** Count the diamonds per cut with one pipe of 5 commands:
    ```
    cut -d, -f2 data/raw/diamonds.csv | tail -n +2 | sort | uniq -c | sort -rn
    ```
    Explain each of the 5 parts in your own words. (`cut`, `sort` and `uniq` are new: guess from the output, then check with `man cut`.)

When you are done: `rm -r ~/practice`, and check with `ls ~` that it is gone.

---

## Answers

Measured on tag `m00` (October 2026).

1. `head -3 data/raw/diamonds.csv`. Columns: `carat,cut,color,clarity,depth,table,price,x,y,z`. The first diamond costs 326.
2. `wc -l data/raw/diamonds.csv` prints `53941`. That is 53,940 diamonds plus 1 header line.
3. `grep -c ",Ideal," data/raw/diamonds.csv` prints `21551`.
4. `grep ",Ideal," data/raw/diamonds.csv > ~/practice/ideal.csv`, then `wc -l ~/practice/ideal.csv` prints `21551`.
5. With `>>` the count becomes `43102`. `>>` adds to the end of the file, so the rows are now there twice. `>` would have replaced the file.
6. `ls -la`. `.gitignore` has 7 lines: `.venv/`, `.env`, `.env.*`, `__pycache__/`, `.ipynb_checkpoints/`, `notebooks/executed/`, `models/`. Git never saves these files. Your virtual environment and any secrets file stay on your laptop.
7. No `x`: the permissions read `-rw-...`. `./scripts/verify_setup.sh` prints `Permission denied`, and `echo $?` prints `126`. The file is not executable. That is why the course always writes `bash scripts/verify_setup.sh`. (`chmod +x` would also fix it, but changes a file in the repo.)
8. An empty line. `export` sets the variable only for the terminal where you typed it and the programs it starts. The second terminal is a separate shell.
9. `command -v aws` (is the `aws` command installed?); lines 16 to 18, `aws sts get-caller-identity ... | "$python" scripts/check_identity.py`; `failures=$((failures + 1))`; `exit 1`.
10. `cut -d, -f2` keeps field 2 (the cut), split on commas. `tail -n +2` skips the header line. `sort` puts equal names next to each other. `uniq -c` counts each run of equal lines. `sort -rn` sorts by that count, biggest first. Result: Ideal 21551, Premium 13791, Very Good 12082, Good 4906, Fair 1610.
