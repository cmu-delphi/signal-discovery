from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_api.serializers import SignalSerializer, AvailableGeographySerializer
from signals.models import Signal, Geography


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


@api_view(
    [
        "GET",
    ]
)
def api_available_geography_view(request, pk):
    """
    API view for getting a single Geography.

    Args:
        request: The request object.
        pk: The primary key of the Geography object.

    Returns:
        Response: The response object.
    """

    try:
        geography = Geography.objects.get(pk=pk)
    except Geography.DoesNotExist:
        return Response(status=404)

    if request.method == "GET":
        serializer = AvailableGeographySerializer(geography)
        return Response(serializer.data)
