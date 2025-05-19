# RoamRadar
RoamRadar is a modern FastAPI web app designed to provide real-time weather information and an AI-powered travel Q&A. It demonstrates production-grade Python app development, CI/CD practices, and modern web tooling for both backend and frontend.
Features

    Weather Dashboard:
    Enter any city to get up-to-date weather stats—temperature, humidity, wind speed, precipitation, pressure, visibility, and more, displayed in a visually appealing dashboard.

    AI Travel Assistant:
    Ask travel-related questions in natural language. The app uses Google Gemini API to generate intelligent answers, rendered in real time.

    Responsive UI:
    Built with Bootstrap 5 and HTMX for snappy, dynamic user interactions.

    Async & Cache:
    Weather API requests are fully async for speed. Results are cached (using DiskCache) for quick repeated queries.

    Clean Code Structure:
    Follows best practices with clear separation between business logic (functions.py) and web handlers (main.py). Environment variables are managed via .env files.

CICD & Code Quality

    Pre-commit Hooks:

        Set up with pre-commit and ruff for automatic code linting and formatting checks before every commit.

        Prevents code with linting errors (e.g., long lines, unused imports) from entering the repository.

    CI/CD Ready:

        Easily integrates with GitHub Actions or any other CI/CD pipeline for linting, testing, and deployment.

        Example CI config checks code formatting and can be extended to run tests and deploy automatically.

Getting Started

    Clone the repo & install dependencies:

git clone https://github.com/yourusername/roamradar.git
cd roamradar
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Configure environment:

    Copy .env.example to .env and fill in your API keys for the weather and Gemini APIs.

Run pre-commit hooks (recommended):

pre-commit install
pre-commit run --all-files

Start the app:

    uvicorn main:app --reload

    Open http://localhost:8000 in your browser.

File Structure

    main.py – FastAPI app, all routing and server logic

    functions.py – All business logic (weather fetching, LLM integration)

    templates/ – Jinja2 HTML templates (index.html, llm_response.html)

    static/ – CSS and frontend assets
