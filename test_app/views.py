from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


@api_view(http_method_names=('POST', 'PUT', 'PATCH'))
def sort_array(request):
    if type(request.data) == str:
        return Response(
            'Incorrect data. Should be array, not string',
            HTTP_400_BAD_REQUEST,
        )
    if isinstance(request.data, dict):
        return Response(
            'Incorrect data. Should be array, not object',
            HTTP_400_BAD_REQUEST,
        )
    numeric_types = (int, float)
    for i in request.data:
        if type(i) not in numeric_types:
            return Response(
                'Incorrect data. Array elements should be numbers',
                HTTP_400_BAD_REQUEST,
            )
    return Response(sorted(request.data))
