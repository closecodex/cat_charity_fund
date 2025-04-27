# QRKot Charity Fund🐈🐱

## Project Description

### QRKot is an API application designed to create charity projects and organize donations for cats.
The fund collects donations for various targeted initiatives: providing medical care for cats in need, setting up shelters for cat colonies, feeding abandoned cats, and supporting any other causes related to feline welfare.

## Installation and Setup

1. **Clone the repository:**
    
    ```bash
    git clone git@github.com:closecodex/cat_charity_fund.git
    cd cat_charity_fund
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv\Scripts\activate
    ```

3. **Upgrade pip and install dependencies:**
   
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
    
    ```bash
    alembic upgrade head
    ```

5. **Start the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

## Example Endpoints

### Authentication

- POST /auth/register — Register a new user.

- POST /auth/jwt/login —  Log in and obtain a JWT token.

### Charity Projects

- GET /charity_project/ — Retrieve a list of all charity projects.

- POST /charity_project/ — Create a new charity project.

### Donations

- GET /donation/my — Get a list of your personal donations.

- POST /donation/ — Make a new donation.

## Additional Information

1. **Author: ([Mariia Osmolovskaia](https://github.com/closecodex/wiki/))**

2. **Technologies: Python, FastAPI, SQLAlchemy, Alembic, SQLite, Pydantic**

3. **API Documentation: [Swagger UI](http://localhost:8000/docs),  [ReDoc](http://localhost:8000/redoc)**
