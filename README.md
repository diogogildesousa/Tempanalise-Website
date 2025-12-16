# Tempanálise Webpage

#### Video Demo: <http://www.youtube.com/watch?v=DSJ6o7b2rBE>

#### Description

The **Tempanálise Webpage** is a full-stack, responsive informational website developed as my CS50x Final Project. The primary goal was to create a modern, user-friendly, and maintainable platform for presenting essential company information, focusing on legal compliance documents, certifications, and client communication. The application features dynamic content loading, aesthetic design elements, and robust input validation.

The system is built on a **Python/Flask** foundation, handling application logic, routing, and database interaction, while the frontend is managed with standard **HTML5, CSS3, and vanilla JavaScript**. Key features include an interactive Dark/Light theme toggle, dynamic content cards styled with a *Glassmorphism* effect, and a fully validated contact form. The ability to manage and provide downloads of important PDF documents (like laws and regulations) from a central database is central to the site’s functionality.

## Design Choices and Justification

The technical implementation of the Tempanálise Webpage was guided by several deliberate design choices:

### 1. Flask Framework
I chose **Flask** for its lightweight and minimalist nature. Given the project's scope—an informational website—a micro-framework was preferred over a full-stack framework like Django. This allowed for greater control over the application structure, minimizing overhead, and focusing development exclusively on the required features (routing, templating, and basic database interaction).

### 2. Database Integration (`site.db`)
A **SQLite** database, named **`site.db`**, was implemented to manage dynamic content. Specifically, the database stores the metadata (titles, dates, file paths) for all certification and legislation records. This design choice ensures that documents can be easily updated or added without directly altering the HTML or application code. This separation of concerns—content from presentation—improves maintainability.

### 3. Frontend Architecture (Mobile-First and Custom CSS)
The entire site was developed using a **mobile-first** approach. This involved writing the base CSS for mobile screens first and then using **CSS Media Queries** to progressively enhance the layout for larger tablets and desktops. This ensures optimal performance and experience across all devices. I deliberately avoided large CSS frameworks like Bootstrap to demonstrate proficiency with pure CSS, allowing for a more unique and customized aesthetic, such as the *Glassmorphism* effect.

### 4. Robust Form Validation
The Contact page form implements both **client-side JavaScript validation** for immediate feedback and **server-side Flask validation** to ensure data integrity. This layered approach is a standard best practice for web security and user experience. The validation specifically checks for a valid email format and a minimum message length.

## File Breakdown

The project repository is structured logically to separate concerns (code, templates, and static assets), as detailed below:

| File/Folder | Purpose and Contents |
| :--- | :--- |
| **`app.py`** | **Main Application Logic.** Contains all Flask routes, database interaction with **`site.db`**, custom error handlers (403, 404, 500), and all server-side form validators. |
| **`site.db`** | **SQLite Database File.** The persistent storage for all dynamic content, including records for legislation, certificates, and submitted contacts. |
| **`requirements.txt`** | **Dependency List.** Lists all Python libraries required to run the project (e.g., `Flask`). |
| **`scripts.js`** | **Client-Side Interactivity.** Manages the mobile **menu hamburguer** functionality, theme toggle logic (Dark/Light Mode), and initial client-side validation for the contact form. |
| **`style.css`** | **Visual Styling.** Contains all CSS rules, variables, and media queries for the entire application, controlling the layout, responsiveness, and aesthetics. |
| **`/fonts`** | **Font Assets.** Stores custom font files used in the design, supplementary to the Roboto font. |
| **`/img`** | **Image Assets.** Repository for all static images, icons, and graphic elements used across the site. |
| **`/pdfs`** | **Document Storage.** Dedicated folder for storing all physical PDF files (legislation and certifications) referenced by the `site.db`. |
| **`templates/`** | **Frontend Templates.** Contains all Jinja2 HTML templates, including: <br> • **`layout.html`**: The base template inherited by all other pages. <br> • **`index.html`**: The homepage content. <br> • **`servicos.html`**: The services page. <br> • **`certificados.html`**: The certifications listing page. <br> • **`legislacao.html`**: The legislation listing page. <br> • **`pdf_viewer.html`**: The template used to display/embed PDF documents. <br> • **`contactos.html`**: The contact form page. <br> • **`403.html`, `404.html`, `500.html`**: Custom error pages. |

## How to Run the Application

To set up and run the **Tempanálise Webpage** in your local environment:

### 1. Prerequisites

Ensure you have **Python 3** installed on your system.

### 2. Setup

git clone <Your-GitHub-Repository-URL-Here>
cd <Your-Project-Folder-Name>
python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies and Initialize Database

pip install -r requirements.txt
Command to initialize the database (e.g., python3 init_db.py or flask shell commands)

### 4. Start the Server
flask run

Access the application in your web browser at http://127.0.0.1:5000/