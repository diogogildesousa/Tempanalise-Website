# Copilot Instructions for Tempanálise Project

## Project Overview
This is a Flask web application for Tempanálise, focused on providing information, document access, and contact forms for a Portuguese business. The app serves static content, PDF documents, and includes a contact form with validation.

## Architecture & Key Components
- **Main entry point:** `app.py` (Flask app, routes, error handlers, form logic)
- **Templates:** Jinja2 HTML files in `templates/` (use `layout.html` for base structure)
- **Static files:** CSS, JS, images, fonts, and PDFs in `static/` subfolders
- **PDFs:** Served from `static/pdfs/` and listed in the legislation page
- **Contact Form:** WTForms-based, with CSRF and flash messaging enabled

## Developer Workflows
- **Run locally:**
  ```bash
  python app.py
  ```
  (Debug mode is enabled by default)
- **Dependencies:**
  - Install with `pip install -r requirements.txt`
  - Key packages: Flask, Flask-WTF, WTForms
- **Formatting:**
  - Use `black` for code formatting (see `requirements.txt`)

## Project-Specific Patterns
- **Routes:** Defined in `app.py`, each page has a dedicated route and template
- **PDF Listing:** PDFs are described in a Python list (`pdfs`) and sorted by date for display
- **Error Handling:** Custom 403, 404, 500 error pages in `templates/`
- **Contact Form:** Validates on POST, flashes success/error, does not send email by default (see comment for extension)
- **Navigation:** Uses active link highlighting via Jinja2 logic in `layout.html`
- **JS/CSS:** Hamburger menu toggling in `static/js/scripts.js`; main styles in `static/css/style.css`

## Integration Points
- **External links:** Footer includes links to IPQ, IPAC, TÜV
- **PDFs:** All legislation PDFs must be placed in `static/pdfs/` and referenced in the `pdfs` list in `app.py`

## Conventions
- **Templates:** Extend `layout.html` for consistent structure
- **Static assets:** Organize by type (css, js, img, fonts, pdfs)
- **Forms:** Use Flask-WTF for all forms, enable CSRF
- **Error pages:** Always use custom templates for error handling

## Example: Adding a New PDF
1. Place the PDF in `static/pdfs/`
2. Add an entry to the `pdfs` list in `app.py` with filename, title, date, and summary

---
For questions about unclear patterns or missing documentation, ask the user for clarification or examples from their workflow.
