---
title: "Git"
date: 2026-05-09
categories:
  - Git
  - Remote
  - SSH
  - Workflow
description: "A practical reference built from real experience — commands, workflows, and solutions that actually came up."
tags:
  - Git
  - VCS (Version Control System)
  - Workflow
reading_time: 3
---

# Git

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By —<strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/git/"><em>Git</em></a>&nbsp;•&nbsp;
         <a href="/categories/github/"><em>GitHub</em></a>&nbsp;•&nbsp;
         <a href="/categories/workflow/"><em>Workflow</em></a>&nbsp;•&nbsp;
      ⏱️ ~3 min read</span>
    </span>
  </div>
</div>

> "Version control is not just a tool — it's a habit."

Git is a **distributed version control system** for tracking changes in files, coordinating work across multiple developers, and reverting to any point in history. GitHub extends that with remote hosting, collaboration, and workflow automation.

This section is a **living reference** — not a tutorial. Every entry here came from a real situation: a merge gone wrong, a stale creation date, a pushed commit that shouldn't have been, a branch tracking the wrong remote. If it happened, it's here.

---

## What's Inside

**[Basics & Daily Commands](basics.md)**

The commands you run every day — init, add, commit, status, .gitignore, aliases, and commit message conventions.

---

**[Branches, Stash & Undoing](branching-stash.md)**

Branching strategies, stash workflows, reverting commits, resetting history, and inspecting specific commits.

---

**[Remotes, GitHub & Workflows](remotes-workflows.md)**

Push, pull, SSH setup, fork workflows, multiple Git identities, divergent branches, and Git LFS.

---

## Quick Reference

The commands you reach for daily — no need to open a full article:

```bash
git status                        # what's going on
git add .                         # stage everything
git commit -m "feat: add thing"   # commit with message
git push                          # push to remote
git pull --rebase                 # pull and keep history linear

git stash push -m "wip/my-work"   # stash with a name
git stash pop                     # apply and drop latest stash
git stash list                    # see all stashes

git log --oneline -10             # last 10 commits at a glance
git diff                          # unstaged changes
git restore --staged .            # unstage everything

git switch -c feat/my-feature     # create and switch to new branch
git merge <branch>                # merge branch into current
git branch -D <branch>            # delete local branch
```

---

## Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [Conventional Commits Spec](https://www.conventionalcommits.org/)
- [gitignore patterns](https://git-scm.com/docs/gitignore)
- [Ignoring files — GitHub Docs](https://help.github.com/en/github/using-git/ignoring-files)
- [Git LFS](https://git-lfs.com/)
- [Revert a pushed commit](https://christoph.ruegg.name/blog/git-howto-revert-a-commit-already-pushed-to-a-remote-reposit.html)
- [Fix non-fast-forward push errors](https://stackoverflow.com/questions/20467179/git-push-rejected-non-fast-forward)