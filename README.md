# User Management API

A scalable and maintainable REST API for managing users, built with Python and FastAPI. This project demonstrates a clean architecture approach, separating concerns into distinct layers for scalability and ease of maintenance.

The API supports creating and retrieving user data, persists data to a JSON file, and includes robust validation for user IDs and Israeli phone numbers.

## Features

- **User Management**: Create and retrieve users.
- **Data Persistence**: User data is saved to and loaded from a `users.json` file.
- **Robust Validation**:
  - Validates user ID format (9 digits).
  - Validates Israeli mobile phone number formats (e.g., 05X-XXXXXXX / 05XXXXXXXX or +9725X-XXXXXXX / +9725XXXXXXXX).
  - Skips invalid user records found in the JSON file on startup without crashing.
- **Clean Architecture**: Code is organized into distinct layers (API, Services, Repositories, Models) for maintainability.
- **Dependency Injection**: Uses FastAPI's dependency injection system to manage a single, shared repository instance, preventing data from being reloaded on every request.
- **Interactive API Docs**: Automatic, interactive API documentation provided by Swagger UI and ReDoc.

## Project Structure

The project follows a clean, layered architecture to separate concerns:

```
.
├── app/                  # Main application package
│   ├── routers/          # API layer (FastAPI routers)
│   ├── repositories/     # Data access layer (repositories)
│   ├── models/           # Pydantic data models (schemas)
│   └── utils/            # Reusable utilities (e.g., validators)
├── main.py               # Application entry point
├── requirements.txt      # Project dependencies
└── users.json            # Data storage file
```

- **`main.py`**: Initializes the FastAPI app and includes the necessary routers.
- **`app/routers/`**: Defines the API endpoints and handles HTTP requests/responses.
- **`app/repositories/`**: Manages data access, abstracting the data source (JSON file).
- **`app/models/`**: Defines the Pydantic data models.
- **`app/utils/`**: Contains shared utilities like data validators.

## Setup and Installation

To run this project locally, follow these steps:

**1. Clone the Repository**

```bash
git clone <repository-url>
cd <repository-folder>
```

**2. Create and Activate a Virtual Environment**
It is recommended to use a virtual environment to manage project dependencies.

- **On macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **On Windows:**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

**3. Install Dependencies**
Install all required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## Running the Application

Once the setup is complete, you can start the API server using Uvicorn. The `--reload` flag enables hot-reloading, which automatically restarts the server when you make code changes.

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:5001`.

## API Endpoints

The API provides the following endpoints for user management:

| Method | Path            | Description                              |
| :----- | :-------------- | :--------------------------------------- |
| `GET`  | `/`             | Returns a welcome message.               |
| `GET`  | `/users/`       | Retrieves a list of all usernames.       |
| `GET`  | `/users/{name}` | Retrieves a specific user by their name. |
| `POST` | `/users/`       | Creates a new user.                      |

### Example: Creating a User

Send a `POST` request to `/users/` with the following JSON body:

```json
{
  "id": "123456789",
  "name": "David Levi",
  "phone": "+972501234567",
  "address": "Herzl 1, Tel Aviv"
}
```

## Interactive API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access it at:

- **Swagger UI**: `http://127.0.0.1:5001/docs`

These interfaces allow you to explore and test all the API endpoints directly from your browser.
