# LinkPost

LinkPost is a Django-based platform for managing and sharing campaign content. The project includes a REST API powered by Django REST Framework and a modern frontend for interacting with the backend services.

## Requirements

- Python 3.11
- pip
- (Optional) Docker 20.10+

All Python package dependencies are tracked in `requirements.txt`.

## Local development

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

The Django admin and API will be available on `http://127.0.0.1:8000/` by default.

## Running tests

Run the Django test suite with:

```bash
python manage.py test
```

## Docker support

The repository ships with a production-ready `Dockerfile`.

Build an image and start the application:

```bash
docker build -t linkpost .
docker run --env DJANGO_SETTINGS_MODULE=campaign_manager.settings \
  --publish 8000:8000 linkpost
```

The container executes `python manage.py runserver 0.0.0.0:8000` by default, exposing the application on port 8000.

## Continuous integration

A GitHub Actions workflow located at `.github/workflows/ci.yml` automatically installs dependencies and performs a syntax check (`python -m compileall .`) on every push and pull request. Use this pipeline as the foundation for more advanced checks such as unit tests, linting, and security scanning.
