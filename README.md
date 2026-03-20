# Third Cage on the Left

**A Memoir by Richard Cansdale**

*Growing up in London Zoo in the 1950s*

This repository now includes a Quarto book workflow that can build the site from the manuscript PDF and publish the rendered output with GitHub Actions for GitHub Pages.

---

Richard Cansdale grew up in an extraordinary place — his family home was inside London Zoo, where his father George Cansdale served as Superintendent. This memoir recounts his childhood adventures among the animals, his father's pioneering work in wildlife television, and the colourful characters they encountered along the way.

📖 **[Read the book online](https://biscoffhamster.github.io/third-cage-on-the-left/)**

---

## About the Author

Richard Cansdale is the son of George Cansdale, the renowned zoologist and broadcaster who became one of Britain's first television wildlife presenters. Richard went on to work in African water development and founded SWF Filtration Ltd, which won a World Business Award for Sustainable Development in 1990.

## About This Project

This book was written during the COVID-19 pandemic lockdown in 2020, as Richard shared his memories with friends and family. It has been compiled and published here by his digital hamster editor, Biscoff.

## Quarto Workflow

The book source can be regenerated from the PDF manuscript with:

```bash
python3 scripts/build_from_pdf.py
quarto render
```

Local renders are written to `_site/`, which is treated as generated output and not committed.

## Editing Workflow

For normal book editing, treat the Quarto files in `book/` as the live manuscript.

1. Edit the relevant chapter file in `book/`.
2. Update `index.qmd` or `_quarto.yml` if you need to change front matter, chapter titles, or chapter order.
3. Preview locally with `quarto preview`, or render with `quarto render`.
4. Commit the source edits and push `main`.

The PDF import script is now a maintenance tool rather than the normal editing path.

- Use `python3 scripts/build_from_pdf.py` only if you want to regenerate chapters from `Page 1 to 10 THIRD CAGE ON THE LEFT.pdf`.
- Regenerating from the PDF can overwrite manual edits in `book/`.
- If a chapter needs editorial improvement, edit the `.qmd` file directly instead of rerunning the importer.

## GitHub Pages Workflow

This repository now includes a GitHub Actions workflow at `.github/workflows/publish.yml` that renders the Quarto book and deploys it to GitHub Pages from source.

Recommended publishing flow:

1. Edit the Quarto source in `book/`.
2. Optionally preview locally with `quarto preview`.
3. Push changes to `main`.
4. GitHub Actions renders the site into `_site/` and deploys it to GitHub Pages.

One-time GitHub configuration:

1. Open the repository settings on GitHub.
2. Go to **Pages**.
3. Set the source to **GitHub Actions**.

You can still run `quarto render` locally when you want to verify the build before pushing. The generated `_site/` directory is disposable and can be removed or regenerated at any time.

---

*Editor: Biscoff (biscoffhamster@gmail.com)*
