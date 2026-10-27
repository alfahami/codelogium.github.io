# Codelogium

> Al-Fahami Toihir's learning journal: notes on CS fundamentals, C, Java, Spring and real-world
> engineering, written while figuring it out.

Live site: [codelogium.com](https://codelogium.com)

---

## What Is This

A personal notes site for what I learn, debug and build as a developer. Not a tutorial site; a
second brain that happens to be public.

Sections: **CS Fundamentals**, **C**, **Languages** (Java), **Lab** (Git; Docker and CI/CD next),
**Projects**, **Blog** and **About**.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [Zensical](https://zensical.org) | Static site generator (Material for MkDocs compatible), pinned in `requirements.txt` |
| Material theme + `overrides/` | Theme, with custom templates for the article, project and blog layouts |
| `awesome-nav`, `blog`, `tags`, `social` | Navigation from `docs/.nav.yml`, blog, tags, and link-preview cards (built in CI only) |
| [GitHub Actions](https://github.com/features/actions) | Builds and deploys on every push to `main` |
| [GitHub Pages](https://pages.github.com/) | Hosting, behind the custom domain |
| Cloudflare | Domain and DNS for codelogium.com (records are **DNS only**, never proxied) |
| Google Analytics + Cloudflare Web Analytics | Traffic stats |
| Google Search Console | Indexing and search performance |

---

## Project Structure

```
codelogium.github.io/
├── docs/
│   ├── index.md                  # Home page
│   ├── .nav.yml                  # Top navigation (tabs) order
│   ├── about/                    # About page, photo, résumé PDF
│   ├── cs-fundamentals/  c/  java/  languages/  lab/  projects/
│   ├── blog/
│   │   ├── index.md
│   │   ├── .authors.yml
│   │   └── posts/                # Blog posts
│   ├── assets/                   # Images (WebP), favicon, flags, share images
│   ├── stylesheets/extra.css     # Colors, layouts, heroes, cards
│   ├── javascript/extra.js       # Footer links, home hero animation
│   ├── CNAME                     # codelogium.com (keep: the deploy rebuilds gh-pages)
│   ├── robots.txt
│   └── google*.html              # Search Console verification (keep)
├── overrides/
│   ├── main.html                 # Titles, link previews, structured data, analytics, home hero
│   ├── blog-post.html            # Blog post layout
│   └── partials/article.html     # Generated header for articles and projects
├── templates/                    # Page templates, helpers and the writing guide
├── new.sh                        # Create pages, convert images, set reading time
├── mkdocs.yml                    # Site configuration
├── requirements.txt              # Python dependencies (Zensical pinned)
└── .github/workflows/ci.yml      # Build and deploy
```

---

## Local Development

```bash
git clone https://github.com/codelogium/codelogium.github.io.git
cd codelogium.github.io
python3 -m venv venv
venv/bin/pip install -r requirements.txt

venv/bin/zensical serve        # http://localhost:8000
```

Run **one** `zensical serve` at a time, and don't run `zensical build` while it's serving: both
write to `site/`, and the server crashes when the folder is wiped.

The image helpers in `new.sh` need Pillow in the system Python (`python3 -m pip install pillow`).

---

## Writing Content

Everything for new pages is in [`templates/`](templates/README.md). The short version:

```bash
./new.sh article java "Java Streams"                          # or: blog "Title", project <group> "Title"
./new.sh img ~/Downloads/streams-flow.png java/java-streams    # screenshots; `photo` for photos and covers
./new.sh readtime docs/java/java-streams.md                    # articles and projects
./new.sh cs50 1 "Talking to the Machine" ~/Documents/notes-images   # CS50 week + notes deck + sidebar
venv/bin/zensical serve                                        # check light, dark and a narrow window
```

`new.sh article|blog|project` creates the file with the title and date filled in; `img` and
`photo` save WebP files under `docs/assets/` and print the Markdown to paste (size and lazy
loading included); `readtime` sets `reading_time` from the word count.

Rules that keep pages fast and clean:

- **Images live in the repo**, added with `new.sh`, never linked from GitHub or elsewhere.
- **Articles and projects have no `# Title` line**: the header is generated from the front matter.
  Blog posts keep it.
- **Short titles** (about 20 characters, keyword first), details in `description`.
- **An `icon:`** on article and project pages only (names at [lucide.dev/icons](https://lucide.dev/icons));
  section and group pages stay plain.
- **`tags:`** from the existing set, for the search filters.
- **A card** on the section page for articles and projects (`new.sh` prints it); blog posts list
  themselves.
- **Track progress** on C and CS Fundamentals: `is-done` / `is-current` on the list items.

[`templates/README.md`](templates/README.md) has the front matter reference, the card snippets,
image rules and how to add a new section.

---

## Publishing

Work happens on the fork (`alfahami/codelogium.github.io`); the live site is built from the org
repo (`codelogium/codelogium.github.io`).

1. Commit and push to the fork's `main`.
2. Open a pull request into the org repo and merge it.
3. GitHub Actions runs `zensical build` and publishes `site/` to the `gh-pages` branch; the site
   updates in a minute or two.
4. For a new page: Search Console, URL Inspection, paste the address, **Request indexing**.

---

## Site Notes

- **Domain:** codelogium.com on Cloudflare. Four `A` records to GitHub Pages
  (185.199.108–111.153) and `www` as a `CNAME` to `codelogium.github.io`, all **DNS only**.
  Proxying them breaks GitHub's HTTPS certificate.
- **Never delete** `docs/CNAME`, the `docs/google*.html` files, or the Cloudflare
  `google-site-verification` TXT record: they keep the domain and Search Console working.
- **Link previews:** most pages get a generated card (brand green, Inter). Pages with
  `social: cards: false` and a `share_image` (home, About) or `cover` share that photo instead.
- **Themes:** light is ink on off-white (`#FAFAF9`, text `#18181B`), dark is near-black; green is
  the accent in both. Colors are tokens at the top of `extra.css`.
- **Analytics:** Google Analytics (`G-9L21ZFFY2J`, also used by the "Was this page helpful?"
  widget) and Cloudflare Web Analytics, loaded in `overrides/main.html`.
- **Upgrading Zensical:** bump the version in `requirements.txt`, reinstall, run a build and check
  the home page, an article, a project and a blog post.

---

## License

See [LICENSE](LICENSE).
