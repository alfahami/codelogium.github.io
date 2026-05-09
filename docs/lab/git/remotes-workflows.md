---
title: "Remotes, GitHub & Workflows"
date: 2026-05-09
categories:
  - Git
  - Workflow
description: "Push, pull, SSH setup, fork workflows, multiple Git identities, divergent branches, skip-worktree, assume-unchanged, LFS, and gist transfer."
tags:
  - Git
  - GitHub
  - Workflow
reading_time: 8
---

# Remotes, GitHub & Workflows

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By —<strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/git/"><em>git</em></a>&nbsp;•&nbsp;
               <a href="/categories/workflow/"><em>workflow</em></a>&nbsp;•&nbsp;
      ⏱️ ~8 min read</span>
    </span>
  </div>
</div>

> "GitHub is a free tool that lets you host your local repository."

---
## Remote Repositories

```bash
git remote                                       # List all linked remote repositories
git remote -v                                    # Verify remotes with URLs
git remote show origin                           # Show URL of remote repository
git remote add origin <url>                      # Add remote via HTTPS
git remote add origin git@github.com:user/repo.git  # Add remote via SSH
git remote set-url origin git@github.com:user/repo.git  # Update remote URL to SSH
git remote remove <name>                         # Remove a linked remote
git push                                         # Push to remote
git push -u origin main                          # Push and set upstream tracking
git pull                                         # Pull latest from remote
git clone <url>                                  # Clone a repository
git push origin +master                          # Remove a commit already pushed remotely
```

---

## Merging a Pull Request Locally

```bash
git pull origin main                             # Step 1: update local repo
git checkout main                                # Step 2: switch to base branch
git merge <branch-name>                          # Step 3: merge the PR branch
git push -u origin main                          # Step 4: push the result
```

---

## Fetch a Single File from Another Branch

Pull one specific file from another branch without merging everything:

```bash
git checkout upstream/<branch> -- path/to/file.java   # overwrite local file with branch version
git checkout HEAD -- path/to/file.java                # undo — restore from current branch
```

The file is overwritten locally and staged automatically.

---

## Ignore Future Changes but Keep the File in the Repo

### assume-unchanged (performance hint)

```bash
git update-index --assume-unchanged <path/to/file>    # git won't notice local edits
git update-index --no-assume-unchanged <path/to/file> # resume tracking
```

!!! warning
    `assume-unchanged` can be silently overwritten by Git during merges and checkouts. Use `skip-worktree` instead for files you actively modify locally.

### skip-worktree (local config files you never want to push)

`.gitignore` only works for untracked files. If a file is already committed, use `skip-worktree`:

```bash
git update-index --skip-worktree path/to/application.properties
git update-index --skip-worktree path/to/logback.xml
```

The file won't appear in `git status`, won't be touched by `git add .`, and won't be committed. Your local changes stay permanently without any effort.

To undo:

```bash
git update-index --no-skip-worktree path/to/application.properties
```

!!! warning
    `skip-worktree` breaks during merges — if the incoming merge touches that file, Git blocks. Workaround:

    ```bash
    cp application.properties application.properties.local.bak   # backup local values
    git update-index --no-skip-worktree application.properties    # lift skip-worktree
    git merge upstream/<branch>                                   # merge
    git update-index --skip-worktree application.properties       # re-apply skip-worktree
    cp application.properties.local.bak application.properties    # restore local values
    echo "*.local.bak" >> .git/info/exclude                       # never track backups
    ```

---

## Adding SSH to GitHub

### Check for existing SSH keys

```bash
ls -al ~/.ssh                                    # list existing SSH keys
```

Default public key filenames: `id_rsa.pub`, `id_ecdsa.pub`, `id_ed25519.pub`

### Generate a new SSH key

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

For legacy systems that don't support Ed25519:

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Press Enter to accept the default file location, then enter a passphrase.

### Add the key to the SSH agent

```bash
eval "$(ssh-agent -s)"                           # start the SSH agent
ssh-add ~/.ssh/id_ed25519                        # add your private key
```

### Copy the public key to GitHub

```bash
sudo apt-get install xclip
xclip -selection clipboard < ~/.ssh/id_ed25519.pub   # copies key to clipboard
```

Then go to GitHub → Settings → SSH and GPG keys → New SSH key → paste → Add SSH key.

---

## Fork Workflow & Remote Tracking

```bash
git remote -v                                    # check all configured remotes
git remote add upstream <url>                    # add upstream when missing
git push origin -u <branch-name>                 # push to fork AND fix tracking
git branch -u origin/<branch-name>               # fix tracking without pushing
git push origin --delete <branch-name>           # delete a remote branch
```

!!! warning
    When you `git switch` to a branch fetched from upstream, Git auto-sets tracking to upstream. Fix it to point to your fork before pushing using `git push origin -u <branch-name>`.

!!! note
    "Write access not granted" on `git push` means your branch is still tracking upstream where you have no write access. Always use `git push origin <branch-name>` explicitly until tracking is fixed.

### Re-fork / Syncing with Upstream

When the upstream repo has new commits you want in your fork:

```bash
git remote add upstream <original-repo-url>      # link to the original repo
git fetch upstream                               # fetch upstream changes
git rebase upstream/master                       # rebase your fork on upstream
```

---

## Multiple Git Identities (Conditional Includes)

Problem: work PC with work credentials, wanting personal project commits attributed to a personal identity.

Solution: Git's `[includeIf]` with `hasconfig:remote.*.url` — switches credentials automatically based on the repo's remote URL, no folder structure required.

**`~/.gitconfig`**

```ini
[user]
    email = work@company.com
    name = Work Name

[includeIf "hasconfig:remote.*.url:git@github.com:yourusername/**"]
    path = ~/.gitconfig-personal

[includeIf "hasconfig:remote.*.url:git@gitea.example.com:yourusername/**"]
    path = ~/.gitconfig-work
```

**`~/.gitconfig-personal`**

```ini
[user]
    email = personal@gmail.com
    name = Personal Name
```

**Useful verification commands:**

```bash
git config --show-origin user.email              # which config file is being used
git config --list --show-origin                  # inspect the full config chain
```

!!! warning
    The `[includeIf]` block must go in `~/.gitconfig`, NOT in `~/.ssh/config`. SSH config only understands Host blocks — mixing them breaks git clone.

---

## Transfer a Gist to GitHub

```bash
git clone https://gist.github.com/<gist-id>     # clone the gist
mv <gist-id>/ gist-github/                      # rename the directory
cd gist-github/
git remote add github https://github.com/<user>/<repo>  # add github as remote
git push github master                           # push to github

# Sync changes going forward
git push github master                           # to GitHub
git push origin master                           # to Gist (origin = gist)

# Clean up remotes
git remote rename origin gist
git remote rename github origin
git remote remove gist
```

---

## Git Large File Storage (LFS)

Git LFS replaces large files (audio, video, datasets, graphics) with text pointers inside Git, while storing the actual file contents on a remote server.

### Setup

```bash
git lfs install                                  # set up LFS once per user account
git lfs track "*.psd"                            # track all .psd files with LFS
git add .gitattributes                           # always track .gitattributes
```

### Migrate existing files to LFS

```bash
git lfs migrate import --include="*.ipynb"       # convert pre-existing files to LFS
```

Then commit and push as normal — LFS handles the rest.

Download LFS: [git-lfs releases](https://github.com/git-lfs/git-lfs/releases)

---

## Revert a Commit Pushed Remotely

Reverting creates a new commit that undoes the bad one — the original commit stays in history but no longer affects the current state.

```bash
git revert <commit-id>                           # safe revert — creates a new commit
```

For reverting a range of commits:

```bash
git revert --no-commit <old-commit>..HEAD
git commit
git push
```

See: [Git HowTo: revert a pushed commit](https://christoph.ruegg.name/blog/git-howto-revert-a-commit-already-pushed-to-a-remote-reposit.html)