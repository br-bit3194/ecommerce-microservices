def parse_serializer_errors(errors_dict):
    """
    Convert serializer.errors into a clean { field: [error1, error2, ...] } structure.
    """
    parsed_errors = {}
    for field, errors in errors_dict.items():
        parsed_errors[field] = [str(error) for error in errors]
    return parsed_errors
