# Third Cage on the Left

**A Memoir by Richard Cansdale**

*Growing up in London Zoo in the 1950s*

This repository now includes a Quarto book workflow that can build the site from the manuscript PDF and publish the rendered output to `docs/` for GitHub Pages.

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

The rendered site is published from `docs/` on the `main` branch via GitHub Pages.

---

*Editor: Biscoff (biscoffhamster@gmail.com)*
