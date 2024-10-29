from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_api.serializers import SignalSerializer
from signals.models import Signal


@api_view(
    [
        "GET",
    ]
)
def api_signal_detail_view(request, pk):
    """
    API view for getting a single Signal object.

    Args:
        request: The request object.
        pk: The primary key of the Signal object.

    Returns:
        Response: The response object.
    """

    try:
        signal = Signal.objects.get(pk=pk)
    except Signal.DoesNotExist:
        return Response(status=404)

    if request.method == "GET":
        serializer = SignalSerializer(signal)
        return Response(serializer.data)
