# Product Service

The `product_service` is responsible for managing product-related operations such as product creation, updates, and retrieval. It provides APIs for managing product details, categories, and inventory.

## Features
- API endpoints for product management.
- CRUD operations for products.
- Category and inventory management.
- Search and filter functionality for products.
- Integration with other services for order and inventory updates.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd product_service
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
   - Copy `.env.backup` to `.env` and update the values as needed.

5. Run the application:
   ```bash
   python manage.py runserver 8001
   ```


## Technologies Used

- **Framework**: Django, Django REST Framework
- **Database**: SQLite (default, can be replaced with PostgreSQL or MySQL)
- **Environment Management**: `python-dotenv`

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```