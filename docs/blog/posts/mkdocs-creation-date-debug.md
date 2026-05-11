---
authors:
  - alfahami
title: "Why My MkDocs Article Showed 11 Months Ago as Creation Date"
date: 2026-05-09
categories:
  - MkDocs
  - Git
  - Debugging
description: "A full debugging story of why a brand new article was showing 11 months ago as its creation date on a MkDocs Material site — and everything I tried before finding the real fix."
reading_time: 8
---

# Why My MkDocs Article Showed 11 Months Ago as Creation Date

> "It's not a bug, it's a debugging story worth writing down."

I created a new article for my MkDocs Material site. Fresh file, new content, committed today. And yet the footer showed:

<!-- more -->

```
🕐 23 hours ago   🕑 11 months ago
```

The update date was correct. The creation date was pointing 11 months into the past. This is the full story of everything I tried before finding the actual fix.

---

## The Setup

My site uses MkDocs Material with the `git-revision-date-localized` plugin to automatically show creation and update dates at the bottom of each page. The config looked like this:

```yaml
plugins:
  - git-revision-date-localized:
      fallback_to_build_date: true
      type: timeago
      enable_creation_date: true
```

---

## What I Tried First — And Why It Didn't Work

### Theory 1: Wrong date in front matter

I had copied an old article as a template. The front matter still had the old `date: 2025-05-07`. I updated it to today's date and the update date changed, but the creation date stayed at 11 months ago.

The `date` field in front matter controls something different from what `git-revision-date-localized` reads. The plugin reads **git history**, not front matter.

### Theory 2: CDN or browser cache

Classic debugging move, hard refresh, clear cache, wait for GitHub Pages to redeploy. Nothing changed. The 11 months persisted.

### Theory 3: Content similarity

I deleted the file and created a brand new one. Still 11 months ago. I even replaced the body with just "Coming soon."; still 11 months ago.

At this point it was clear this wasn't a cache issue.

---

## Finding the Real Cause — Git History

Running `git log` without `--follow` on the new file showed only one clean commit from today. No old history.

But with `--follow`:

```bash
git log --all --follow --oneline -- docs/blog/post/network/network1.md
```

The output traced all the way back to commits from May 2025: 11 months ago. Git was following the file's rename history across remotes and linking it to the old `generic-types.md` article I had copied from.

The culprit was the **upstream remote**. I had a fork setup with an `upstream` remote still configured, and the plugin was scanning commits from that remote's history:

```
864e78b (upstream/main, upstream/HEAD) Update generic-types.md
```

---

## The Fixes I Applied

### Fix 1: follow_renames: false

The plugin docs mention a `follow_renames` option. I added it:

```yaml
- git-revision-date-localized:
    enable_creation_date: true
    follow_renames: false
```

It didn't work, the option wasn't recognized in my plugin version. The correct option was:

```yaml
- git-revision-date-localized:
    enable_creation_date: true
    enable_git_follow: false
```

This helped with future files but didn't fix the current one because the upstream remote was still there with its full history.

### Fix 2: Remove the upstream remote

```bash
git remote remove upstream
git push origin main
```

This was the real fix. Once the upstream remote was gone, the plugin had no old history to trace back to and correctly showed today as the creation date.

---

## But Wait — Dates Still Weren't Showing

Even after fixing the git history issue, some pages weren't showing any dates at all. The plugin was running, the files were committed, but the footer was empty.

Inspecting the page source revealed the `.md-source-file` element was there in the DOM — but hidden. 

The culprit was in `extra.css`:

```css
/* Hide contributors and feedback sections by default */
.md-source-file,
.md-feedback {
  display: none !important;
}
```

And in `extra.js`, dates were only shown on pages matching `/blog/` in the URL:

```javascript
const isBlogPage = path.includes('blog');

if (isBlogPage) {
  document.body.classList.add('show-contrib-feedback');
}
```

My new article was under `/lab/git/`, no `blog` in the URL, so dates were hidden by design. The fix was updating the JS to show dates on all content pages:

```javascript
const overviewSlugs = ['/', '/network/', '/databases/', '/java/', '/spring/', '/lab/', '/blog/', '/categories/', '/tags/'];
const isOverviewPage = overviewSlugs.includes(path)
  || path.endsWith('/index.html')
  || ['categories', 'tags'].some(p => path.includes(p));

if (!isOverviewPage) {
  document.body.classList.add('show-contrib-feedback');
}
```

---

## Summary of Root Causes

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Creation date 11 months ago | Upstream remote with old git history | `git remote remove upstream` |
| `follow_renames: false` not working | Wrong option name | Use `enable_git_follow: false` |
| Dates not showing on Lab pages | `extra.js` only enabled dates for `/blog/` URLs | Update JS condition to cover all content pages |

---

## Key Takeaways

- `git-revision-date-localized` reads **git history**, not front matter dates
- `--follow` in git can trace history across remotes, old remotes you forgot about can affect plugin behavior
- The correct option to disable follow behavior is `enable_git_follow: false`, not `follow_renames: false`
- If dates aren't showing at all, check your CSS and JS, the plugin might be injecting them correctly but they're hidden
- Deleting and recreating a file won't help if the upstream remote still has old history for that path

---

## Collateral Discoveries

Along the way I also learned:

- `git log --all --follow` vs `git log`, the `--all` flag includes all remotes, `--follow` traces renames. Use both when debugging date issues
- The `git-committers` plugin and `git-revision-date-localized` are separate — one handles author avatars, the other handles dates. They can fail independently
- MkDocs `--dirtyreload` flag is useful for faster local development but can serve stale plugin data, sometimes a full restart is needed

---

If you're hitting the same "wrong creation date" issue on your MkDocs Material site, start by checking your remotes:

```bash
git remote -v
git log --all --follow --oneline -- path/to/your/file.md
```

Chances are the answer is in there.