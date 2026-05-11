---
title: "Branches, Stash & Undoing"
date: 2026-05-09
categories:
  - Git
  - Workflow
description: "Branching strategies, stash workflows, reverting commits, resetting history, and inspecting specific commits."
tags:
  - Git
  - Branches
  - Stash
  - Revert
reading_time: 6
---
# Branches, Stash & Undoing

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By —<strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/git/"><em>Git</em></a>&nbsp;•&nbsp;
               <a href="/categories/workflow/"><em>Workflow</em></a>&nbsp;•&nbsp;
      ⏱️ ~6 min read</span>
    </span>
  </div>
</div>

> "A branch is a lightweight movable pointer to one of these commits."

---

## Branches

A branch is a lightweight movable pointer to a commit. Creating a branch means creating a new pointer to move around. `main` (or `master`) is the default branch.

### Branch Commands

```bash
git branch <name>                                # Create a new branch
git switch -c <name>                             # Create and switch to new branch
git checkout -b <name>                           # Same as above (older syntax)
git checkout <name>                              # Switch to a branch
git branch -a                                    # List all local and remote branches
git branch -r                                    # List only remote branches
git show-branch                                  # List branches with their commits
git rev-parse --abbrev-ref HEAD                  # Show current branch name only
git branch -m old-name new-name                  # Rename a branch
git branch -D <name>                             # Delete a local branch
git push origin <name>                           # Push and create remote branch
git push origin --delete <name>                  # Delete a remote branch
git branch --set-upstream-to=origin/<name>       # Set branch to track remote
git push --set-upstream origin <name>            # Push and set upstream in one command
```

### Merging

```bash
git merge <branch> # Merge branch into current (be on target branch)
```

---

## Branch Naming — Sub-branches Don't Exist in Git
Git has no concept of sub-branches. The `/` in a branch name is just a string character, purely a human convention for visual grouping.

```bash
feat/FeatureName
test/feat/FeatureName     # only "related" by name — Git has no idea
```

Git sees both as equal, independent branches. The naming is for **you**, not for Git.

### Common Naming Conventions

```bash
feat/<feature-name>        # new feature
fix/<bug-description>      # bug fix
refactor/<scope>           # refactoring
chore/<task>               # maintenance
test/<what-youre-testing>  # local test branches
```

---

## Moving Uncommitted Work to a New Branch

If you made changes on the wrong branch:

```bash
git switch -c feat/correct-branch               # uncommitted changes travel with you
git add .
git commit -m "feat: your message"
```

If you already committed on the wrong branch:

```bash
git reset --soft HEAD~1                          # undo commit, keep changes staged
git switch -c feat/correct-branch
git commit -m "feat: your message"
```

---

## Git Stash

!!! note
    Uncommitted changes live in the **working directory and staging area**, not in a specific branch. Always stash before switching branches when work is still in progress.

### Basic Stash Commands

```bash
git stash                                        # Stash current changes
git stash push -m "message"                      # Stash with a descriptive name
git stash list                                   # List all stashes
git stash apply                                  # Apply latest stash (keeps it in list)
git stash apply <index>                          # Apply a specific stash by index
git stash pop                                    # Apply and drop latest stash
git stash pop <index>                            # Apply and drop specific stash
git stash drop <index>                           # Delete a specific stash
git stash clear                                  # Delete all stashes
```

### Stash Naming Convention

Always name stashes with a prefix for clarity:

```bash
git stash push -m "local/properties-logback"    # config files reused across branches, never pushed
git stash push -m "wip/<branch>-description"    # WIP code tied to a specific branch
git stash push -m "test/what-youre-testing"     # local test data only
git stash push -m "drop/whatever"               # marked for deletion
```

**Golden rules:**

- Keep **one** `local/` config stash total, pop it, use it, re-stash it. Never duplicate
- Never commit with local config applied, re-stash before `git push`
- Never mix `wip/` and `local/` in the same stash; stash them separately
- Drop a `wip/` stash as soon as its branch is merged

### Renaming a Stash

Git has no native rename command — pop and re-stash:

```bash
git stash pop stash@{N}                          # pop the one to rename
git stash push -m "proper/name"                  # re-stash with the correct name
```

### Inspecting a Stash Before Applying

```bash
git stash show -p stash@{N}                      # full diff of stash N
git show stash@{N}:path/to/file                  # see one specific file from a stash
git diff stash@{N} -- path/to/file               # compare stash version vs current
```

### Applying Only Specific Files from a Stash

```bash
git checkout stash@{0} -- path/to/file.java      # cherry-pick one file from a stash
```

---

## Undoing & Reverting

### Revert a Commit (Safe — Creates a New Commit)

Reverting creates a new commit that undoes the changes of a previous one. The original commit stays in history.

```bash
git revert <commit-id>                           # revert a specific commit
```

### Revert a Repository to a Previous Commit

```bash
git revert --no-commit 0766c053..HEAD
git commit
git push
```

### Delete the Last Commit Locally and Remotely
```bash
git reset HEAD^ --hard                           # reset local branch to parent commit
git push origin -f                               # force push to remote
```

Or using the commit hash directly:

```bash
git push origin +<commit-hash>^:master           # force remote to parent of that commit
```

### Delete a Local Commit (Interactive Rebase)

```bash
git rebase -i HEAD~x                             # x = number of commits back to edit
```

In the editor, change `pick` to `drop` for the commit you want to remove.

---
## Git Prune

Cleans up unreachable or orphaned git objects and outdated remote branch references:

```bash
git prune                                        # clean up unreachable objects
git fetch --all --prune                          # fetch and clean outdated remote branches
```

---
## Divergent Branches on Pull

Happens when two sources commit to the same branch (e.g. you locally + GitHub Actions). Git refuses to pull without knowing how to reconcile.

Fix permanently:

```bash
git config --global pull.rebase true             # always rebase instead of merge on pull
```

For a one-time fix:

```bash
git pull --rebase origin <branch-name>
```

---

---

## Cherry-pick

Apply a specific commit from any branch to your current branch without merging everything:

```bash
git cherry-pick <commit-hash>                    # apply one specific commit
git cherry-pick <hash1> <hash2> <hash3>          # apply multiple commits in order
git cherry-pick <hash1>..<hash2>                 # apply a range of commits
```

!!! tip "Real use case"
    Your branch picked up commits you didn't make (contaminated branch). Start fresh and bring only your work:
    ```bash
    git checkout <base-branch>
    git checkout -b feat/clean-branch            # fresh branch from base
    git cherry-pick <your-commit-hash>           # bring only your commit(s)
    git push origin feat/clean-branch
    ```
    This is cleaner than trying to untangle a messy branch history.

!!! warning
    Cherry-pick replays commits; if the commit touches files that have changed since, you may get conflicts to resolve manually.

---

## Abort a Merge or Rebase in Progress

If a merge or rebase goes wrong and you want to get back to a clean state:

```bash
git merge --abort                                # abort an in-progress merge
git rebase --abort                               # abort an in-progress rebase
```

Both commands restore your branch to the state it was in before you started. Safe to run at any point during a conflict resolution.

!!! note
    If you accidentally closed your terminal mid-rebase and git is still in rebase state, check with `git status`: it will tell you a rebase is in progress. Then run `git rebase --abort` to clean up.

---

## Diagnose a Contaminated Branch

When your branch has commits you didn't make, usually because it was created from an old or wrong base:

```bash
git log base-branch..your-branch --oneline      # commits in your branch not in base
git diff base-branch..your-branch --name-only   # files that differ between branches
```

If you see commits you didn't make, start clean:

```bash
git checkout <base-branch>
git checkout -b feat/clean-branch               # fresh branch from correct base
git checkout feat/OldBranch -- path/to/your/file.java  # bring only your files
git commit -m "feat: port changes to clean branch"
git push origin feat/clean-branch
```

## Ways of Resolving `git push rejected non-fast-forward`

Start with:

```bash
git pull origin
```

If that doesn't work, fetch and rebase manually:

```bash
git fetch origin feature/my-branch:tmp           # fetch remote branch to tmp
git rebase tmp                                   # rebase on it
git push origin HEAD:feature/my-branch           # push rebased changes
git branch -D tmp                                # clean up temp branch
```

Or the simpler approach:

```bash
git fetch
git rebase feature/my-branch
git push origin feature/my-branch
```

See more approaches [here](https://stackoverflow.com/questions/20467179/git-push-rejected-non-fast-forward).