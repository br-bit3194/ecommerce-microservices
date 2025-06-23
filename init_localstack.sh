#!/bin/bash
set -e

echo "Waiting for LocalStack SQS..."

# Wait for SQS to be ready
until curl -s http://localstack:4566/_localstack/health | grep '"sqs": "running"' > /dev/null; do
  sleep 2
done

echo "Creating SQS queues..."
awslocal sqs create-queue --queue-name order-queue
awslocal sqs create-queue --queue-name payment-queue

echo "Queues created."
