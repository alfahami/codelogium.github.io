# Codelogium

> Developer logs, notes, and learning paths; built with MkDocs Material.

Live site: [codelogium.github.io](https://codelogium.github.io)

---

## What Is This

A personal documentation site covering things I learn, debug, and build as a developer. Not a tutorial site; more of a second brain that happens to be public.

Sections include Java, Spring, Databases, Network, Lab (Git, Docker, CI/CD), and a Blog for stories and reflections.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) | Static site framework and theme |
| [GitHub Pages](https://pages.github.com/) | Hosting and deployment |
| [GitHub Actions](https://github.com/features/actions) | CI/CD pipeline for auto-deploy on push |
| [git-revision-date-localized](https://github.com/timvink/mkdocs-git-revision-date-localized-plugin) | Shows creation and update dates on pages |
| [git-committers](https://github.com/ojacques/mkdocs-git-committers-plugin-2) | Shows contributor avatars on pages |
| [mkdocs-categories-plugin](https://github.com/eddyluten/mkdocs-categories-plugin) | Auto-generates category pages from front matter |
| [mkdocs-blogging-plugin](https://liang2kl.github.io/mkdocs-blogging-plugin/) | Blog index and pagination |
| Google Analytics (GA4) | Traffic and engagement tracking |
| Google Search Console | SEO and sitemap submission |

---

## Project Structure

```
codelogium.github.io/
├── docs/
│   ├── index.md              # Home page
│   ├── blog/
│   │   ├── index.md          # Blog overview
│   │   └── posts/            # Blog articles (managed by blog plugin)
│   ├── databases/            # Database articles
│   ├── java/                 # Java articles
│   ├── lab/
│   │   └── git/              # Git reference articles
│   ├── network/              # Network articles
│   ├── spring/               # Spring articles
│   ├── categories/           # Auto-generated category pages
│   ├── assets/               # Images and static files
│   ├── stylesheets/
│   │   └── extra.css         # Custom styles
│   └── javascript/
│       └── extra.js          # Custom JS (controls date/contributor visibility)
├── .github/
│   └── workflows/            # GitHub Actions deployment pipeline
├── mkdocs.yml                # MkDocs configuration
├── requirements.txt          # Python dependencies
└── README.md
```

---

## Local Development

### Prerequisites

- Python 3.x
- pip

### Setup

```bash
# Clone the repo
git clone https://github.com/codelogium/codelogium.github.io.git
cd codelogium.github.io

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run locally

```bash
python -m mkdocs serve
```

Site will be available at `http://127.0.0.1:8000`

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `MKDOCS_GIT_COMMITTERS_APIKEY` | GitHub personal access token for the git-committers plugin. Prevents API rate limiting during local development. Needs `public_repo` scope. |

Set it for your local session:

```bash
# Windows
set MKDOCS_GIT_COMMITTERS_APIKEY=your_token_here

# Mac/Linux
export MKDOCS_GIT_COMMITTERS_APIKEY=your_token_here
```

For the live deployment, this is set as a repository secret in GitHub Actions.

---

## Deployment

Deployment is fully automated via GitHub Actions. Every push to `main` triggers a build and deploy to GitHub Pages.

The workflow file is at `.github/workflows/`. No manual deployment needed; just push and the site updates automatically.

---

## Writing Content

### Adding a new article

1. Create a `.md` file in the appropriate section folder (e.g. `docs/java/my-article.md`)
2. Add front matter:

```yaml
---
title: "Your Article Title"
date: 2026-05-09
categories:
  - Java
description: "A short description for SEO and meta tags."
reading_time: 5
---
```

3. Add it to `nav` in `mkdocs.yml`
4. Commit and push

### Adding a blog post

1. Create a `.md` file under `docs/blog/posts/`
2. Add front matter with at minimum `title` and `date`
3. Add `<!-- more -->` after the intro paragraph to set the excerpt shown on the blog index
4. Add `authors: - alfahami` if you have authors configured
5. Add it to `nav` in `mkdocs.yml`

### Front matter reference

```yaml
---
title: "Article Title"           # Page title and SEO title
date: 2026-05-09                  # Publication date (used by git plugin)
categories:                       # Auto-generates category pages
  - Git
  - Workflow
description: "SEO description"    # Used for meta description tag
reading_time: 5                   # Shown in blog-meta div (minutes)
---
```

---

## Page Boilerplates

Ready-to-use starter templates for every page type. Click to expand and copy.

<details>
<summary>📄 Section Index</summary>

For overview pages like `java/index.md`, `network/index.md`, etc.

```markdown
---
title: <Section Name>
description: "<Short description of what this section covers.>"
hide:
  - toc
  - navigation
  - feedback
  - metadata
  - footer
---

# <Emoji> <Section Name>

<One or two sentences describing what this section is about and who it's for.>

---

## Posts

- [Article Title](article-slug.md)  
  _Short one-line description of what the article covers._

*(More posts coming soon...)*
```

</details>

<details>
<summary>🧪 Lab Section Index</summary>

For tool overview pages like `lab/git/index.md`.

```markdown
---
title: "<Tool Name>"
date: YYYY-MM-DD
categories:
  - <Category>
  - Workflow
description: "<One sentence describing this tool reference.>"
reading_time: <N>
---

# <Tool Name>

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By: <strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/<category>/"><em><category></em></a>&nbsp;•&nbsp;
      ⏱️ ~<N> min read</span>
    </span>
  </div>
</div>

> "<A short quote.>"

<One or two sentences describing what this section covers and why it exists.>
This section is a **living reference**, not a tutorial. Every entry came from a real situation.

---

## What's Inside

**[<Article 1 Title>](<article-1.md>)**

<Short description.>

---

**[<Article 2 Title>](<article-2.md>)**

<Short description.>

---

## Quick Reference

```bash
command                                          # description
```

---

## Resources

- [Resource Name](url)
```

</details>

<details>
<summary>📖 Lab Reference Article</summary>

For technical cheatsheet pages like `lab/git/basics.md`.

```markdown
---
title: "<Article Title>"
date: YYYY-MM-DD
categories:
  - <Category>
  - Workflow
description: "<One sentence describing what this article covers.>"
reading_time: <N>
---

# <Article Title>

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By: <strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/<category>/"><em><category></em></a>&nbsp;•&nbsp;
      ⏱️ ~<N> min read</span>
    </span>
  </div>
</div>

> "<A short quote or key idea that sets the tone.>"

---

## <First Section>

<Content here.>

```bash
command                                          # description
```

---

## <Second Section>

<Content here.>
```

</details>

<details>
<summary>☕ Regular Technical Article</summary>

For articles like `java/generic-types.md` or `network/basic-network1.md`.

```markdown
---
title: "<Article Title>"
date: YYYY-MM-DD
categories:
  - <Category>
description: "<One sentence describing the article for SEO.>"
reading_time: <N>
---

# <Article Title>

<div class="blog-meta">
  <div class="blog-meta-container">
    <span class="meta-content">
      By: <strong><a href="https://github.com/alfahami" target="_blank">Al-Fahami Toihir</a></strong>
      &nbsp; <span class="category-timer-mobile"> 🏷️&nbsp;<a href="/categories/<category>/"><em><category></em></a>&nbsp;•&nbsp;
      ⏱️ ~<N> min read</span>
    </span>
  </div>
</div>

> "<A short quote or key idea.>"

<Intro paragraph.>

---

## <First Section>

<Content here.>

---

## What We Learned

<Short summary of key takeaways.>
```

</details>

<details>
<summary>📝 Technical Blog Post</summary>

For narrative articles under `blog/posts/`.

```markdown
---
authors:
  - alfahami
title: "<Article Title>"
date: YYYY-MM-DD
categories:
  - <Category>
description: "<One sentence describing the article for SEO.>"
---

# <Article Title>

> "<A short quote that captures the spirit of the article.>"

<One paragraph intro that sets up the problem or story.>

<!-- more -->

<Rest of the article content here.>

---

## <First Section>

<Content here.>
```

</details>

---

## Key Configuration Notes

### git-revision-date-localized

```yaml
- git-revision-date-localized:
    fallback_to_build_date: true
    type: timeago
    enable_creation_date: true
    enable_git_follow: true       # traces file history through renames
    exclude:
      - index.md
      - network/index.md
      - java/index.md
      - spring/index.md
      - databases/index.md
      - lab/index.md
```

- `enable_git_follow: true` preserves original creation dates when files are moved
- Section index pages are excluded to avoid showing incorrect dates on overview pages

### Date and contributor visibility (extra.js)

Dates and contributor avatars are hidden by default via CSS and shown only on content pages via JavaScript. Overview/index pages don't show them. The logic is in `docs/javascript/extra.js`.

### Categories

Categories are auto-generated from the `categories:` field in front matter by the `mkdocs-categories-plugin`. Add new category pages to the `Categories` nav section in `mkdocs.yml` when introducing a new category.

---

## SEO Setup

- **Google Analytics**: GA4 property `G-9L21ZFFY2J` configured in `mkdocs.yml`
- **Google Search Console**: Site verified and sitemap submitted at `sitemap.xml`
- **Sitemap**: Auto-generated by MkDocs at `https://codelogium.github.io/sitemap.xml`
- **Meta tags**: `title` and `description` front matter fields are automatically injected as `<meta>` tags by MkDocs Material

---

## Dependencies

All Python dependencies are listed in `requirements.txt`. Install with:

```bash
pip install -r requirements.txt
```

Current dependencies:

```
mkdocs-material
mkdocs-awesome-pages-plugin
mkdocs-blogging-plugin
mkdocs-git-revision-date-localized-plugin
mkdocs-git-committers-plugin-2
mkdocs-categories-plugin
```