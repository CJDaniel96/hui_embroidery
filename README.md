# Hui Embroidery Website (湘繡)

A personal brand website for Master Hui and family, showcasing the art of Xiang Embroidery. Built with **Wagtail CMS**, **Django**, and **Tailwind CSS**.

## Design Philosophy

The website follows a "Atmospheric, Minimalist, Detail-oriented" (大氣、留白、強調細節) design philosophy to highlight the embroidery works, similar to an art museum's white walls.

## Tech Stack

- **Backend**: Django 5.2+, Wagtail 6.2+
- **Frontend**: Tailwind CSS (via `django-tailwind`)
- **Database**: PostgreSQL (via Docker)
- **Infrastructure**: Docker Compose

## Development Setup

### Prerequisites

- Docker Desktop installed and running.

### Quick Start

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd hui_embroidery
    ```

2.  **Build and Run with Docker**:
    ```bash
    docker compose up -d --build
    ```

3.  **Initialize Tailwind CSS** (First time only):
    The project is set up to run Tailwind via the `theme` app.
    ```bash
    docker compose exec web python manage.py tailwind install
    docker compose exec web python manage.py tailwind build
    ```

4.  **Create Admin User**:
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

5.  **Access the Site**:
    - **Frontend**: http://localhost:8000
    - **Admin**: http://localhost:8000/admin

## Project Structure

- `home/`: Main landing page application.
- `about/`: Biography and studio introduction.
- `gallery/`: Portfolio work management (WorkPage, GalleryIndexPage).
- `contact/`: Contact form and location.
- `theme/`: Tailwind CSS configuration and source files.

## Styling

Styles are managed via `django-tailwind`. Edit `theme/static_src/src/styles.css` or use utility classes directly in templates.
To watch for changes during development:
```bash
docker compose exec web python manage.py tailwind start
```
(Note: In the current Docker setup, `runserver` handles Django, but you may need to rebuild CSS if adding new classes that were not previously generated, or run the watcher.)
