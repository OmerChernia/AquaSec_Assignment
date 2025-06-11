# User Management API

A scalable and maintainable REST API for managing users, built with Python and FastAPI. This project demonstrates a clean architecture approach, separating concerns into distinct layers for scalability and ease of maintenance.

The API supports creating and retrieving user data, persists data to a JSON file, and includes robust validation for user IDs and Israeli phone numbers.

## Features

- **User Management**: Create and retrieve users.
- **Data Persistence**: User data is saved to and loaded from a `users.json` file.
- **Robust Validation**:
  - Pydantic models enforce data shape and constraints (e.g., ID length).
  - Custom validation logic for Israeli mobile phone number and ID formats.
  - Skips invalid user records found in the JSON file on startup without crashing.
- **Clean Architecture**: Code is organized into distinct layers for maintainability.
- **Dependency Injection**: Uses FastAPI's dependency injection system to manage a single, shared repository instance.
- **Interactive API Docs**: Automatic, interactive API documentation provided by Swagger UI.

## Project Structure

The project follows a clean, layered architecture to separate concerns:

```
.
├── app/                  # Main application package
│   ├── routers/          # API layer (FastAPI routers)
│   ├── repositories/     # Data access layer (repositories)
│   ├── models/           # Pydantic data models (data shape)
│   └── utils/            # Reusable utilities (e.g., specific format validators)
├── tests/                # Test suite
│   ├── test_api.py       # API endpoint tests
│   └── test_users.json   # Data used exclusively for testing
├── main.py               # Application entry point
├── requirements.txt      # Project dependencies
└── users.json            # Data storage file
```

- **`main.py`**: Initializes the FastAPI app and includes the necessary routers.
- **`app/routers/`**: Defines the API endpoints and handles HTTP requests/responses.
- **`app/repositories/`**: Manages data access, abstracting the data source (JSON file).
- **`app/models/`**: Defines the Pydantic data models.
- **`app/utils/`**: Contains shared, specific utility functions.

## Prerequisites

- **Python 3.9+** (Python 3.11 is recommended)
- **git** for cloning the repository

## Setup and Running the Project (Linux)

Here are the precise instructions to get the project running on a Linux system.

**1. Clone the Repository**
If you haven't already, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-folder>
```

**2. Setup and Run with a Single Command Block**
The following commands will create a virtual environment, activate it, install the required dependencies, and start the application server. You can copy and paste this entire block into your terminal.

```bash
# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Run the application with Uvicorn
# The --reload flag enables hot-reloading for development
echo "Starting the application server..."
uvicorn main:app --host 127.0.0.1 --port 5001 --reload
```

The API will now be running and available at `http://127.0.0.1:5001`.

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

This interface allows you to explore and test all the API endpoints directly from your browser.

## Testing

This project uses `pytest` for testing. The tests are located in the `tests/` directory and are configured to run in an isolated environment using the `tests/test_users.json` data file, so they won't affect your primary `users.json`.

To run the tests, first ensure you have installed the project dependencies:

```bash
# Make sure your virtual environment is activated
pip install -r requirements.txt
```

Then, run `pytest` from the root of the project directory:

```bash
pytest -v
```

The `-v` flag enables verbose output, showing which tests passed or failed.
