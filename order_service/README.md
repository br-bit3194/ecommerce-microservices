# Order Service

The `order_service` is responsible for managing order-related operations such as creating, updating, and retrieving orders. It integrates with the `payment_service` to handle payment requests and notifications using AWS SQS.

## Features

- Create, update, and retrieve orders.
- Integration with `payment_service` for payment initiation.
- Notification to `payment_service` using AWS SQS for initiating payment requests.
- Logging and error handling for order operations.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd order_service
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
   - Copy `.env.backup` to `.env` and update the values as needed:
     ```dotenv
     DATABASE_URL=sqlite:///db.sqlite3
     AWS_ACCESS_KEY_ID=your-aws-access-key-id
     AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
     AWS_SQS_QUEUE_URL=your-sqs-queue-url
     ```

5. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Run the application:
   ```bash
   python manage.py runserver 8002
   ```

## Notification to Payment Service
- The `order_service` sends a notification to the `payment_service` to initiate a payment request. This is done using AWS SQS by sending a message with the order and payment details.

Start order service polling SQS:
```bash
  python manage.py poll_sqs
```

## Swagger Documentation
- The API documentation is available at `http://localhost:8002/swagger/` after running the server.

## API Endpoints

### Order Operations
- `POST /api/orders/` - Create a new order.
- `GET /api/orders/<id>/` - Retrieve a specific order.

[//]: # (- `PUT /api/orders/<id>/` - Update an order.)

[//]: # (- `DELETE /api/orders/<id>/` - Delete an order.)

## Technologies Used

- **Framework**: Django, Django REST Framework
- **Database**: SQLite (default, can be replaced with PostgreSQL or MySQL)
- **Environment Management**: `python-dotenv`
- **Logging**: Python `logging` module
- **AWS SQS**: For message queuing and notification to the `payment_service`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
```