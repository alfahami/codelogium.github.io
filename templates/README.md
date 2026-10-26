# Adding new content

Templates and helpers for new pages. They live outside `docs/`, so they're never published.

## The short version

```bash
./new.sh article java "Java Streams"                          # 1. create the page
./new.sh img ~/Downloads/streams-flow.png java/java-streams    # 2. add screenshots (prints the Markdown)
#    ...write, add a card (section 4)...
./new.sh readtime docs/java/java-streams.md                    # 3. set reading_time
venv/bin/zensical serve                                        # 4. check http://localhost:8000
git add docs && git commit -m "docs: add Java Streams" && git push   # 5. publish, then merge the PR
```

## 1. Create the file

From the repo root:

```bash
./new.sh article java "Java Streams"          # -> docs/java/java-streams.md
./new.sh blog "My Claude Certification"       # -> docs/blog/posts/my-claude-certification.md
./new.sh project java "Banking App"           # -> docs/projects/java/banking-app.md
```

The title and today's date are filled in. Then fill in `description`, `categories`, `tags` and `icon`,
delete the HTML comment, and write.

**Titles:** keep them to about 20 characters so they fit on one line in the sidebar
("Daily Commands", "Java Generics"). The detail goes in `description`. Keep the main keyword in
the title, since it's also the Google result title.

## 2. What goes in the front matter

| Field | Article | Blog post | Project | What it does |
|---|---|---|---|---|
| `title` | yes | yes | yes | Page title, sidebar entry, search result title |
| `date` | yes | yes | yes | Shown in the header (projects show the year) |
| `categories` | yes | yes | yes | Pills in the header; blog categories also group posts |
| `description` | yes | yes | yes | Text under the title and in search results |
| `reading_time` | yes | no | yes | Minutes; set it with `./new.sh readtime`. Blog posts get it calculated |
| `icon` | yes | no | yes | Sidebar icon, e.g. `lucide/terminal` (names at https://lucide.dev/icons). Pages only: section and group `index.md` pages get none |
| `tags` | yes | yes | yes | Search filters. Reuse the existing set: Git, Tooling, Debugging, Java, Spring, Microservices, Blockchain, MkDocs; add C, CS50, K&R once those notes exist |
| `repo`, `stack` | | | yes | GitHub button and stack pills |
| `demo`, `year` | | | optional | "Live demo" button; overrides the year |
| `cover`, `cover_alt`, `cover_focus` | optional | optional | optional | Wide photo at the top of the header |

The one rule that matters: **articles and projects have no `# Title` line** (the header is
generated). **Blog posts keep it**, because the blog page uses it for the card title.

## 3. Images

Always keep images in the repo, never linked from GitHub or elsewhere. `new.sh` converts them to
WebP under `docs/assets/<dir>/` and prints the Markdown to paste, with the size filled in:

```bash
./new.sh img   ~/Downloads/login-form.png projects/banking-app   # screenshots, diagrams
./new.sh photo ~/Downloads/desk.jpg posts                         # photos, covers
```

| | `img` (screenshots) | `photo` (photos, covers) |
|---|---|---|
| Size | kept as is, so small text stays sharp | capped at 1200px wide |
| Quality | 90 | 85 |
| Typical file | 15–70 KB | 100–250 KB |

The printed line looks like this; the width and height let the browser reserve the space, and
`loading=lazy` loads the image only when the reader scrolls to it:

```markdown
![Login form](/assets/projects/banking-app/login-form.webp){ width="1366" height="737" loading=lazy }
```

Write a real alt text in place of `Alt text`: it's what screen readers and Google see.

## 4. Add a card (articles and projects only)

Blog posts appear on the blog page by themselves. Articles and projects need a card on their
section page; `new.sh` prints it ready to paste. Cards use Zensical's grid cards, inside the
section's grid:

```markdown
-   :lucide-braces:{ .lg .middle } __Java Generics__

    ---

    How generics work across interfaces, classes and multi-type scenarios, with real examples.

    ---

    [Read article :lucide-arrow-right:](generic-types/)
```

- Use the page's own `icon` so the card and the sidebar match.
- Keep the description to one or two lines (about 120–160 characters).
- The link text is `Read article` for notes and `View project` for projects.

Where they go:

| Page | Card goes in | Notes |
|---|---|---|
| Java article | `docs/java/index.md` and `docs/languages/index.md` | Languages links with `/java/<slug>/` |
| Lab guide | `docs/lab/index.md` | its own section page lists its pages too, like `docs/lab/git/index.md` |
| Project | `docs/projects/index.md` (right group) and `docs/projects/<group>/index.md` | href `<group>/<slug>/` on the Projects page |

The accent color comes from the wrapper the cards sit in, so a new card picks it up by itself.
For a new grid, wrap it like this (pick the class for the section: `--lang`, `--lab`, `--c`,
`--cs`; on the Projects page each group's `id` sets its color):

```html
<div class="project-sections project-sections--lang" data-search-exclude markdown>

<div class="grid cards" markdown>

...cards...

</div>

</div>
```

**Home page (optional):** to feature something under "Latest notes", copy one of the
`home-mini-card` blocks in `docs/index.md` and change the link, kicker, title and text.

### Track progress (C and CS Fundamentals)

The K&R, Beej's, CS50 and Teach Yourself CS panels in `docs/c/index.md` and
`docs/cs-fundamentals/index.md` are checklists:

- Finished item: `<li class="is-done">Arrays</li>` (filled check)
- Current item: `<li class="is-current">Algorithms</li>` (half circle, bold)
- Update the counter in the meta line, e.g. `3 / 10 weeks`.
- The panel you're currently working on has `track-panel--featured` (the moving border light).
- When a notes page exists, replace the "coming soon" placeholder with the button in the HTML
  comment just above it.

## 5. A new section

If the article starts a new section (say `docs/python/`), the section also needs an `index.md`
(copy `docs/java/index.md` and change the hero text; section pages have no `icon`) and a line in `docs/.nav.yml` to
show it in the top navigation.

## 6. Preview and publish

```bash
venv/bin/zensical serve      # http://localhost:8000, one server at a time
```

Check the page in both light and dark mode, and on a narrow window. Then:

```bash
git add docs/
git commit -m "docs: add Java Streams"
git push
```

The push goes to the fork; open the PR into the org repo and merge it, and GitHub Actions
deploys codelogium.com in a minute or two. For a new page, ask Google to index it: Search Console,
URL Inspection, paste the address, Request indexing.
