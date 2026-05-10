---
title: "Basics & Daily Commands"
date: 2026-05-09
categories:
  - Git
  - Workflow
description: "The git commands you use every day — init, add, commit, status, .gitignore, aliases, and commit message conventions."
tags:
  - Git
  - Basics
  - Commands
  - Commit
reading_time: 5
---

# Basics & Daily Commands

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By —<strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/git/"><em>git</em></a>&nbsp;•&nbsp;
               <a href="/categories/workflow/"><em>workflow</em></a>&nbsp;•&nbsp;

      ⏱️ ~5 min read</span>
    </span>
  </div>
</div>

> "You decide when to take a snapshot by making a commit."

---

## What is Git

Git is a **Version Control System (VCS)** for tracking changes in computer files.

- Distributed version control
- Coordinates work between multiple developers
- Tracks who made what changes and when
- Allows reverting back to any point in time
- Supports both local and remote repositories

---

## Core Concepts

- Keeps track of code history
- Takes **snapshots** of your files
- You decide when to take a snapshot by making a **commit**
- You can visit any snapshot at any time
- You can **stage** files before committing

---

## Local Repository Commands

```bash
git init                                         # Initialize local git repository
git add <file>                                   # Add a file to the staging area
git add .                                        # Add all files to the staging area
git add *.extension                              # Add all files with a specific extension
git status                                       # Check status of working tree
git commit                                       # Commit changes (opens editor)
git commit -m 'message'                          # Commit with inline message
git commit -a --allow-empty-message -m ''        # Commit with no message
git reset HEAD <file>                            # Unstage a specific file
git rm --cached <file>                           # Remove a file from the staging area
git restore --staged .                           # Unstage everything
git restore -S .                                 # Shorthand for unstage everything
git checkout -- <file>                           # Discard changes in working directory
```

---

## Git Configuration

```bash
git config --global user.name 'Your Name'        # Set your name
git config --global user.email 'your@email.com'  # Set your email
git config --global credential.helper store      # Store credentials permanently
git config --global credential.helper cache      # Cache credentials for a session
git config --global credential.helper 'cache --timeout=600'  # Cache with timeout
git config --global pull.rebase true             # Always rebase on pull (linear history)
```

---

## Amending Commits

### Change the last commit message

```bash
git commit --amend                               # Opens editor to change last commit message
git commit --amend -m "New commit message"       # Change inline without opening editor
```

!!! tip
    Make sure you have no staged changes before amending, or they'll be included in the commit.

### Amend the last commit author

```bash
git commit --amend --reset-author --no-edit      # Fix author of last commit
git log -1 --pretty=format:"%an <%ae>"           # Verify the author is correct
git push --force-with-lease                      # Force push safely after amend
```

---

## .gitignore

Contains all files and folders you don't want tracked in your repository. Create a `.gitignore` file in the root of your repo and list files or patterns to ignore.

```bash
# Example .gitignore entries
*.log
*.env
node_modules/
target/
.idea/
```

??? tip "Other ways to ignore files"

    - Add entries to `.git/info/exclude` — works like `.gitignore` but stays local and never shows in `git status`
    - `.gitignore` can ignore itself, but adding it to `.git/info/exclude` is cleaner

See the [official gitignore documentation](https://git-scm.com/docs/gitignore) and [GitHub's guide on ignoring files](https://help.github.com/en/github/using-git/ignoring-files) for pattern syntax.

---

## Git Aliases

Aliases let you create shortcuts for long or frequently used commands. Configure them in `~/.gitconfig` or `.git/config`:

```bash
git config --global alias.co checkout           # git co instead of git checkout
git config --global alias.st status             # git st instead of git status
git config --global alias.lg "log --oneline"    # git lg for compact log
```

Or edit `~/.gitconfig` directly:

```ini
[alias]
    co = checkout
    st = status
    lg = log --oneline
```

---

## Commit Message Convention

Using a consistent commit message format keeps your git history clean and readable. The most widely used convention is **Conventional Commits**.

### Structure

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### Commit Types

| Type | Purpose |
|------|---------|
| `feat` | Introduces a new feature |
| `fix` | Fixes a bug |
| `refactor` | Code change that doesn't fix a bug or add a feature |
| `chore` | Maintenance tasks (e.g., updating dependencies) |
| `docs` | Documentation updates |
| `test` | Adds or updates tests |
| `style` | Formatting (spaces, indentation — no code changes) |
| `perf` | Performance improvements |
| `ci` | Changes to CI/CD pipeline |
| `build` | Changes affecting the build system or dependencies |

### Examples

```bash
feat(auth): add JWT token refresh endpoint
fix(portfolio): resolve NPE when fetching holdings
refactor(repository): improve query performance for holdings lookup
docs(readme): update setup instructions
chore: bump spring-boot to 3.2.1
```

### Best Practices

- Use **imperative mood** — "Add method" not "Added method"
- Keep the title **under 50 characters**
- Add context in the body when necessary

---

## Inspecting History

```bash
git log                                          # Full commit history
git log --oneline -10                            # Last 10 commits, compact
git log --oneline -- path/to/file                # History of a specific file
git log --all --follow --oneline -- file         # Follow renames across history
git show <commit-hash>                           # Full diff of a commit
git show <commit-hash> --stat                    # Files changed in a commit
git show <commit-hash> -- path/to/file           # Specific file from a commit
git diff                                         # Unstaged changes
git diff --staged                                # Staged changes
```

---

## Inspecting Code Authorship

```bash
git blame <file>                                 # show who wrote each line and when
git blame -L 381,381 <file>                      # blame a specific line only
git blame -L 100,120 <file>                      # blame a range of lines
```

??? tip "Real Use Case"
    When a build breaks and you need to find who introduced the change:
```bash
    git blame -L 381,381 src/main/java/com/example/MyService.java
    # fab986cd (Nitika Garg 2026-04-27 13:42:47 +0530 381) problematic code here
```
    You get the commit hash, author name, timestamp, and the exact line —
    enough to track down who made the change and when, then cross-reference with `git show`:
```bash
    git show fab986cd                            # see the full diff of that commit
    git show fab986cd --stat                     # just the files changed
```