---
title: "Issues & Troubleshooting"
date: 2026-05-11
categories:
  - Git
  - Workflow
description: "Real git issues encountered during development; root causes, investigation steps, and fixes."
reading_time: 8
---

# Issues & Troubleshooting

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By: &nbsp;<strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/git/"><em>git</em></a>&nbsp;•&nbsp;
               <a href="/categories/workflow/"><em>workflow</em></a>&nbsp;•&nbsp;
      ⏱️ ~8 min read</span>
    </span>
  </div>
</div>

> "When git behaves unexpectedly, the answer is almost always in the history."

A personal log of real git issues encountered during development; root causes, investigation steps, and fixes. Not theory — things that actually happened.

---

## 1. Merge Blocked by skip-worktree File

### Problem

```
error: Your local changes to the following files would be overwritten by merge:
        path/to/SomeFile.java
Please commit your changes or stash them before you merge.
Aborting
```

### Investigation

```bash
git diff path/to/SomeFile.java                   # nothing
git diff HEAD path/to/SomeFile.java              # nothing
git diff --cached path/to/SomeFile.java          # nothing

# Compare against upstream
git diff upstream/<branch> -- path/to/SomeFile.java
# Result: only a trailing newline difference, harmless
```

### Root Cause

```bash
git ls-files -v path/to/SomeFile.java
# Output: S path/to/SomeFile.java
```

`S` prefix means the file is marked with `--skip-worktree`. Git still detects the upstream conflict despite the flag.

### Fix

```bash
git update-index --no-skip-worktree path/to/SomeFile.java
git merge upstream/<branch>
```

Re-apply after merge:

```bash
git update-index --skip-worktree path/to/SomeFile.java
```

### Notes

- Always check `git ls-files -v <file>` when git behaves unexpectedly on a specific file
- `S` = skip-worktree (intentional local override, survives resets)
- `h` = assume-unchanged (performance hint, weaker)

---

## 2. Setting up skip-worktree for Local Config Files

### Problem

Config files like `application.properties` and `logback.xml` contain local environment values that should never be committed, but git keeps picking them up.

### Solution

```bash
git update-index --skip-worktree path/to/application.properties
git update-index --skip-worktree path/to/logback.xml

# Add logs folder to local gitignore (invisible to teammates)
echo "logs/" >> .git/info/exclude
```

### Verify it worked

```bash
git status                                       # those files should NOT appear
```

### Common Mistake

```bash
# WRONG: git reads the whole thing as one path
git update-index --skip-worktree application.properties git update-index --skip-worktree logback.xml
# fatal: Unable to mark file git

# CORRECT: run separately
git update-index --skip-worktree application.properties
git update-index --skip-worktree logback.xml
```

### Limitation

`skip-worktree` does NOT fully protect against merges. If the incoming merge touches that file, Git blocks. Fix:

```bash
git update-index --no-skip-worktree application.properties
git stash
git merge upstream/<branch>
git stash pop
# manually restore your local values
git update-index --skip-worktree application.properties
```

---

## 3. Merge Conflicts with Teammates' Changes

### Problem

```
CONFLICT (content): Merge conflict in path/to/SomeConstants.java
CONFLICT (content): Merge conflict in path/to/SomeService.java
Automatic merge failed; fix conflicts and then commit the result.
```

### Root Cause

Multiple developers modified the same lines in the same files. Git cannot decide which version to keep.

### Resolution Strategy

Open each conflicted file and look for conflict markers:

```
<<<<<<< HEAD          # your version starts here
your changes
=======               # separator
their changes
>>>>>>> upstream      # their version ends here
```

Three cases:

- **Keep yours**: delete from `<<<<<<< HEAD` to `=======` and the closing `>>>>>>>`
- **Keep theirs**: delete from `<<<<<<< HEAD` to `=======` and keep theirs
- **Merge both**: manually combine the two versions (most common for shared constants/config files)

After resolving all files:

```bash
git add .
git commit -m "merge: resolve conflicts with upstream"
```

### Nuclear Option (discard all local changes)

```bash
git fetch upstream <branch>
git reset --hard upstream/<branch>
git push --force origin <branch>
```

!!! warning
    This permanently loses all your local commits. See issue #7 for the safer version.

---

## 4. Stash Conflict on Pop

### Problem

After `git stash pop`, conflicts appear because the stash was saved on a different branch state.

### Fix — Abort and get back to clean

```bash
git restore --staged .
git restore .
```

### Useful Stash Commands

```bash
git checkout stash@{0} -- path/to/file           # apply only one file from stash
git diff stash@{0} -- path/to/file               # preview stash contents before applying
git show stash@{0}:path/to/file                  # see one specific file from stash
git stash drop stash@{0}                         # drop after applying
git stash push -m "wip/description"              # named stash for clarity
```

---

## 5. Fetching a Single File from Upstream

### Use Case

You have a branch with lots of local modifications. You only want one specific file from upstream without touching anything else.

### Solution

```bash
git fetch upstream <branch>                      # update local references
git checkout upstream/<branch> -- path/to/file.java  # pull only that file
```

### Notes

- This **overwrites** your local version of that file with no warning
- The file is automatically staged; just `git commit` after
- To undo: `git checkout HEAD -- path/to/file`

---

## 6. Moving Uncommitted Changes to a New Branch

### Case 1: Changes not yet committed

```bash
git checkout -b feat/correct-branch             # uncommitted changes travel with you
git add .
git commit -m "feat: my changes"
```

### Case 2: Already committed on wrong branch

```bash
git reset --soft HEAD~1                          # undo commit, keep changes staged
git checkout -b feat/correct-branch
git commit -m "feat: my changes"
```

### Case 3: Extra safe approach

```bash
git stash push -m "wip/moving-to-new-branch"
git checkout -b feat/correct-branch
git stash pop
```

---

## 7. Reset Branch to Match Upstream Exactly

### Use Case

You want your branch to match upstream exactly; discard all local commits and changes.

```bash
git fetch upstream <branch>
git reset --hard upstream/<branch>
git push --force origin <branch>
```

!!! warning
    All local commits are permanently lost.

### Safer version — save work first

```bash
git stash push -m "wip/before-reset"
git fetch upstream <branch>
git reset --hard upstream/<branch>
git stash pop
# resolve any conflicts
git add .
git commit -m "feat: reapply changes on top of upstream"
git push origin <branch>
```

---

## 8. SSH Post-Quantum Warning on git fetch

### Problem

```
** WARNING: connection is not using a post-quantum key exchange algorithm.
** This session may be vulnerable to "store now, decrypt later" attacks.
```

### Root Cause

The remote server is using a classical key exchange algorithm (ECDH). This is a theoretical future risk only.

### Fix

Nothing to fix on your end; this is a server-side configuration issue. Your connection is still encrypted. The `git fetch` itself completed successfully. Ask your GitHub Enterprise admin to upgrade the SSH config if needed.

---

## 9. PR Closed After Upstream Rebase

### Problem

Maintainer rebased the base branch, GitHub rewrote commit hashes, and your PR was automatically closed.

### Fix

```bash
git fetch upstream <new-base-branch>
git checkout -b feat/resubmit-branch upstream/<new-base-branch>
git cherry-pick <your-commit-hash>               # bring your changes over
git push origin feat/resubmit-branch
```

Then open a new PR from `feat/resubmit-branch` and close the old one.

---

## 10. Inspecting What Changed

```bash
git show <commit-hash>                           # full diff of a commit
git show <commit-hash> --stat                    # file names only
git show <commit-hash> -- path/to/file           # one file only
git diff upstream/<branch> -- path/to/file       # diff between your branch and upstream
git ls-files -v path/to/file                     # check file tracking status
```

File tracking status prefixes in `git ls-files -v`:

- `S` = skip-worktree
- `h` = assume-unchanged
- blank = normal tracking

---

## Quick Reference: skip-worktree vs assume-unchanged

| | `--skip-worktree` | `--assume-unchanged` |
|---|---|---|
| Prefix in `git ls-files -v` | `S` | `h` |
| Use case | Intentional local config override | Performance hint for large files |
| Survives `git reset` | Yes | No |
| Blocks merge if upstream touches file | Yes | Yes |
| Recommended for config files | Yes | No |

