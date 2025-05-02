import logging

class CorrelationIdFilter(logging.Filter):
    def filter(self, record):
        # You can access the correlation_id from the request or context here.
        # In this case, we're assuming it's being passed through extra context.
        # Make sure you set `correlation_id` in the log record when logging.
        correlation_id = getattr(record, 'correlation_id', 'N/A')
        record.correlation_id = correlation_id
        return True

def parse_serializer_errors(errors_dict):
    """
    Convert serializer.errors into a clean { field: [error1, error2, ...] } structure.
    """
    parsed_errors = {}
    for field, errors in errors_dict.items():
        parsed_errors[field] = [str(error) for error in errors]
    return parsed_errors

