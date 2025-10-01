This project is a Flask-based REST API developed as part of the Laboratory 1 of the Distributed Systems and Networks course. The goal is to design and implement an API that manages a movie database while integrating with an external API.


## Environment Setup

- Creation of a Python virtual environment using venv.
- Installation of dependencies from requirements.txt.

### Movie Management API

- Implementation of CRUD operations for movies (create, read, update, delete).
- Support for searching movies by title or genre.
- Endpoints to suggest random movies, including suggestions filtered by genre.
- External API Integration
- Connection with the noLaborables API to retrieve upcoming holidays in Argentina.
- Recommendation of movies for the next holiday, optionally filtered by genre.

### Testing and Validation

- Unit testing using pytest and custom test scripts.
- Manual testing with curl and Postman.
- Evaluation of API responses, HTTP status codes, scalability, and security aspects.
