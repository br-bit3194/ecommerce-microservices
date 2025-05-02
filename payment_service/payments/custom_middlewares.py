import uuid

class CorrelationIdMiddleware:
    """
    Middleware to ensure every request has an 'X-Correlation-ID' header.
    If not present, it generates a new one.
    """

    CORRELATION_ID_HEADER = 'X-Correlation-ID'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get existing correlation id or generate new one
        correlation_id = request.headers.get(self.CORRELATION_ID_HEADER)

        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        # Save it to request (you can use later if needed)
        request.correlation_id = correlation_id

        # Process the request
        response = self.get_response(request)

        # Add correlation id to response headers
        response['X-Correlation-ID'] = correlation_id

        return response
