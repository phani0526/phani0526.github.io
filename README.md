# phani0526.github.io

My profile site, live at **https://phani0526.github.io**.

All content lives in Markdown files. Edit a file, push to `main`, and GitHub
rebuilds and publishes the site in a minute or two.

## Where things are

```
content/
  profile.md          name, tagline, contact links, career line, intro text
  sections/
    01-about.md       one file per section; the number sets the order
    02-speaking.md
    ...
assets/               resume.pdf, photo, any other files to publish
theme/                template.html, style.css (colours, fonts), site.js
build.py              turns the Markdown into the site (no need to edit)
```

## Editing content

**Change text:** open the file in `content/` and edit it. Normal Markdown works:
`**bold**`, `*italic*`, `[link](https://...)`, `- bullet lists`.

**Each section file starts with settings between `---` lines:**

```yaml
---
title: Speaking and workshops   # heading on the page
nav: Speaking                   # label in the sidebar (optional)
layout: entries                 # prose | entries | bios | tags
lead: One-line intro under the heading (optional)
hidden: true                    # hide the section without deleting it
---
```

**Layouts:**

| layout    | what it does                                                     |
|-----------|------------------------------------------------------------------|
| `prose`   | plain text                                                       |
| `entries` | each `### Heading` becomes its own row, heading on the left      |
| `bios`    | like entries, with a "Copy text" button on each                  |
| `tags`    | each `### Heading` with its bullet list shown as chips           |

In `entries`, a grey detail line under a heading is written like this:

```markdown
### Juniper Networks

Software Engineer 3, Jul 2023 – present · Bengaluru
{: .meta }
```

**Add a section:** create a new file such as `content/sections/05-talks-given.md`.
**Reorder:** rename the number prefixes. **Remove:** delete the file or set `hidden: true`.

**Photo:** put an image in `assets/` (e.g. `assets/photo.jpg`, square, ~400×400)
and set `photo: assets/photo.jpg` in `content/profile.md`.

**Resume:** replace `assets/resume.pdf` with the new file, keeping the name.

**Colours and fonts:** the variables at the top of `theme/style.css`.

## Preview on your laptop (optional)

```bash
pip install -r requirements.txt
python build.py --serve
```

Then open http://localhost:8000. Re-run after each edit.

## Publishing

`.github/workflows/deploy.yml` builds and deploys on every push to `main`.
One-time setup: repo **Settings → Pages → Source: GitHub Actions**.
