# User Service

The `user_service` is responsible for managing user-related operations such as authentication, user profile management, and authorization. It provides APIs for user registration, login, profile updates, and more.

## Features
- API endpoints for user management.

## Future features:
- User registration and login (supports JWT or session-based authentication).
- CRUD operations for user profiles.
- Password hashing and security.
- Role-based access control (if applicable).


## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd user_service
    ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - copy .env.backup to .env and update the values as needed.

5. Run the application:
   ```bash
   python manage.py runserver 8000
   ```
   
## Swagger Documentation
- The API documentation is available at `http://localhost:8000/swagger/` after running the server.