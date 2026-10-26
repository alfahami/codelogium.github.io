---
title: "Git"
date: 2026-05-09
categories:
  - Git
  - Workflow
description: "A practical reference built from real experience; commands, workflows, and solutions that actually came up."
reading_time: 3
cover: assets/posts/git.webp
cover_alt: "A git logo sticker held between two fingers"
cover_focus: center 86%
cover_ratio: 1200 / 380
cover_share: assets/posts/git.jpg
social:
  cards: false
tags:
  - Git
  - Tooling
---

> "Version control is not just a tool; it's a habit."

Git is a **distributed version control system** for tracking changes in files, coordinating work across multiple developers, and reverting to any point in history. Remote platforms like GitHub, GitLab, or Gitea extend that with hosting, collaboration, and workflow automation.

This section is a **living reference**, not a tutorial. Every entry here came from a real situation: a merge gone wrong, a stale creation date, a pushed commit that shouldn't have been, a branch tracking the wrong remote. If it happened, it's here.

---

## What's Inside

<div class="project-sections project-sections--lab" markdown>

<div class="grid cards" markdown>

-   :lucide-terminal:{ .lg .middle } __Daily Commands__

    ---

    The commands you run every day: init, add, commit, status, .gitignore, aliases and commit conventions.

    ---

    [Read article :lucide-arrow-right:](basics.md)

-   :lucide-git-branch:{ .lg .middle } __Branches & Stash__

    ---

    Branching strategies, stash workflows, reverting commits, resetting history and inspecting commits.

    ---

    [Read article :lucide-arrow-right:](branching-stash.md)

-   :lucide-git-pull-request:{ .lg .middle } __Remotes & Workflows__

    ---

    Push, pull, SSH setup, fork workflows, multiple Git identities, divergent branches and Git LFS.

    ---

    [Read article :lucide-arrow-right:](remotes-workflows.md)

-   :lucide-bug:{ .lg .middle } __Troubleshooting__

    ---

    Real git issues from development: root causes, investigation steps and fixes.

    ---

    [Read article :lucide-arrow-right:](issues.md)

</div>

</div>

---

## Quick Reference

The commands you reach for daily; no need to open a full article:

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
- [Ignoring files - GitHub Docs](https://help.github.com/en/github/using-git/ignoring-files)
- [Git LFS](https://git-lfs.com/)
- [Revert a pushed commit](https://christoph.ruegg.name/blog/git-howto-revert-a-commit-already-pushed-to-a-remote-reposit.html)
- [Fix non-fast-forward push errors](https://stackoverflow.com/questions/20467179/git-push-rejected-non-fast-forward)