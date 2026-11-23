# Git mini exercise

This folder records the commands and answers for the linked Git practice. Run the practice in a new, disposable local directory. For the final push step, create your own empty GitHub repository and substitute its URL; do not reuse a repository that contains work you need.

## Setup and first commits

```bash
git --version
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
mkdir my-first-repo && cd my-first-repo
git init -b main
printf '# My first repository\n' > readme.txt
git status
git add readme.txt
git commit -m "Add readme file"
git log --oneline
```

After editing `readme.txt`, `git status` reports it as modified but unstaged. Stage and commit it:

```bash
git add readme.txt
git commit -m "Document project purpose"
git log --oneline
```

`git diff` shows unstaged changes; `git log --oneline` summarizes commits. `git status` reports the working tree and staging area.

## Branch, script, merge

```bash
git branch
git branch feature-script
git switch feature-script
git switch -c dev
git switch feature-script
git branch --show-current
```

Create `install.sh` on `feature-script` and choose a package appropriate for your OS. The sample below uses apt on Debian/Ubuntu:

```bash
cat > install.sh <<'SCRIPT'
#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' 'Starting installation...'
sudo apt-get update
sudo apt-get install -y tree
printf '%s\n' 'Installation complete!'
SCRIPT
chmod +x install.sh
git add install.sh
git commit -m "Add install script"
git log --oneline
git switch main
ls
git merge feature-script
ls
git log --oneline --graph --decorate
git branch -d feature-script
```

Before merging, `install.sh` is absent from `main`; after the merge it is present. A fast-forward merge may not create a separate merge commit. The feature branch can be deleted after its changes are integrated.

## Push and clone

Create an empty public GitHub repository named `my-first-repo` in your own account, without initializing a README. Then use its actual URL:

```bash
git remote add origin https://github.com/YOUR-USERNAME/my-first-repo.git
git push -u origin main
cd ..
git clone https://github.com/YOUR-USERNAME/my-first-repo.git
```

Avoid deleting the remote GitHub repository just to repeat the exercise. To practice again safely, use a new local directory and a different temporary GitHub repository. The original exercise's destructive delete step is described here rather than automated.

## Reflection

- Version control keeps a history, supports parallel work, and makes changes reviewable and reversible.
- Staging selects the exact changes for the next snapshot; committing records that snapshot in local history.
- Commit when a coherent, reviewable unit of work is complete.
- `git init` creates a new local repository; `git clone` copies an existing repository and its history.
- Clear commit messages let collaborators understand why a change was made.
- Branches isolate work so experiments and features can progress without destabilizing the main line.
- Create a branch for work that should be developed and reviewed separately, such as a feature or bug fix.
