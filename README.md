# Thyme Inn portfolio

Plain HTML and CSS. No build step.

## Files

- `index.html` – page content
- `style.css` – styling; colours and fonts are variables at the top
- `downloads/Thyme-Inn-CV.pdf` – one-page CV linked from the site
- `downloads/Thyme-Inn-Slides.pdf` – six-slide deck linked from the site
- `tools/build_pdfs.py` – regenerates both PDFs from editable content

## Customise

1. Replace the sample headline, intro, projects and contact details in `index.html`.
2. Edit the CONTENT section at the top of `tools/build_pdfs.py` (experience, results, skills, links), then run:

       pip install reportlab
       python tools/build_pdfs.py

   Commit the updated files in `downloads/`.
3. Change colours in the variables at the top of `style.css`.

## Gotham

Gotham is a paid font, so it is not bundled. Until you add it, the site uses Montserrat, a free look-alike.

- **Website:** buy a web font licence from Typography.com, then either add the exported files as `fonts/Gotham-Book.woff2`, `fonts/Gotham-Medium.woff2` and `fonts/Gotham-Bold.woff2` (the `@font-face` rules in `style.css` already point there), or use the CSS link Typography.com gives you.
- **PDFs:** put `Gotham-Book.ttf`, `Gotham-Medium.ttf` and `Gotham-Bold.ttf` in a `fonts/` folder and re-run `build_pdfs.py`. Without them the PDFs use Helvetica.

## Deploy with GitHub and Netlify

1. Create a GitHub repository and upload these files (keep the folders).
2. In Netlify, choose **Add new site → Import an existing project** and connect GitHub.
3. Pick the repository, leave the build command empty and set the publish directory to `/`.
4. Select **Deploy**. Every push to GitHub redeploys the site.

The contact form works on Netlify without extra setup. Submissions appear under **Forms** in your dashboard.

## Language and theme toggles

- The header has an EN / BM switch and a light / dark button. Both choices are remembered in the visitor's browser.
- The page opens in Malay by default. To open in English instead, change `"ms"` to `"en"` in the small script in the `<head>` of `index.html`.
- Dark mode follows the visitor's device setting until they press the button.
- The English text is the normal text in `index.html`. Each translated element carries its Malay beside it as `data-ms="..."`. Edit both when you change a sentence, and add `data-ms` to any new text.
- The CV and slide PDFs are English only.
