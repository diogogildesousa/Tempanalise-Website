## Technical Architecture and Project Flow

The **Tempanálise Webpage** utilizes the Python **Flask** micro-framework to manage all backend logic and routing, adhering to a clear separation of concerns. The core controller is **`app.py`**, which is responsible for:

1.  **Route Definition:** Handling all endpoint requests, including `/`, `/servicos`, `/ceritificados`, `/legislacao`, and `/contactos`.
2.  **Database Interaction:** Connecting to the **`site.db`** SQLite file to fetch dynamic content (e.g., certification listings, law records).
3.  **Validation:** Implementing server-side checks for the contact form submissions.
4.  **Error Handling:** Defining custom handlers for status codes 403, 404, and 500, rendering the respective HTML templates.

All HTML pages (Views) are built upon the **`layout.html`** base template using Jinja2 templating. This ensures consistency in the navigation structure, theme toggles, and footer across all nine application pages, preventing code duplication.

## Database and File Management

### The `site.db` and `/pdfs` Interaction
The application's dynamic data resides in the **`site.db`** SQLite database. This database is critical for managing the lists of services, certificates, and legislation. Instead of storing the large PDF documents directly, the database stores the **metadata** and the **relative file path** to the documents.

For example, the database table for legislation contains a field that points to a specific file within the **`/pdfs`** directory.

The **`/pdfs`** folder is dedicated to storing all physical document files. When a user wants to view a document, the application:
1.  Fetches the file path from `site.db`.
2.  Uses the Flask route to securely access the file.
3.  Renders the **`pdf_viewer.html`** template, which embeds or displays the content of the linked PDF. This keeps the data management clean and file retrieval secure.

### Error Handling System
To provide a polished and professional user experience, the application includes custom templates for the three most common error codes, all defined and triggered within **`app.py`**:
* **`403.html` (Forbidden):** Rendered when a user attempts to access a resource they are not authorized to view.
* **`404.html` (Not Found):** Rendered for any undefined route.
* **`500.html` (Internal Server Error):** A graceful fallback for unhandled exceptions, ensuring the user is not met with a default, unfriendly browser error page.

## Frontend Implementation Details

### Styling and Interactivity
All visual styling, including the responsive layout, color variables for theming, and the *Glassmorphism* effects, are contained exclusively in **`style.css`**. The use of a single, well-organized CSS file allows for centralized maintenance of the entire look and feel.

The client-side interactivity is managed by **`scripts.js`**. This includes essential components such as:
* The **Hamburger Menu** functionality for mobile navigation.
* Client-side form validation on the **`contactos.html`** page.
* The persistence logic for the Dark/Light theme selection (likely using Local Storage).

### Asset Management
* The **`/fonts`** folder contains custom fonts, allowing for consistent typography even without an internet connection, complementing the primary **Roboto** font loaded from Google Fonts.
* The **`/img`** folder centrally manages all images, icons, and static graphical assets used across the various templates.

This comprehensive separation ensures that the application is easy to debug, scale, and maintain over time.