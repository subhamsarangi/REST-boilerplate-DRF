from rest_framework.views import exception_handler
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    {
        "detail": "Given token not valid for any token type",
        "code": "token_not_valid",
        "messages": [
            {
                "token_class": "AccessToken",
                "token_type": "access",
                "message": "Token is invalid or expired"
            }
        ]
    }
    """
    response = exception_handler(exc, context)

    if response is not None:
        if response.status_code == status.HTTP_403_FORBIDDEN:
            response.data = {
                'detail': response.data.get('detail', 'You do not have permission to perform this action.'),
                'status': response.status_code
            }
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            response.data = {
                'detail': 'Authentication failed.',
                'code': 'token_not_valid',
                'messages': [
                    {
                        'message': 'The provided token is either invalid or expired. Please check your token and try again.'
                    }
                ],
                'status': response.status_code
            }

    return response