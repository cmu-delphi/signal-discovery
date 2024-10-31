from rest_framework.serializers import ModelSerializer, SlugRelatedField

from signals.models import Signal, Geography


class SignalSerializer(ModelSerializer):
    """
    Serializer for the Signal model.
    """

    source = SlugRelatedField(read_only=True, slug_field="name")
    signal_type = SlugRelatedField(read_only=True, slug_field="name")
    available_geography = SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Signal
        fields = ["name", "source", "signal_type", "available_geography", "time_type"]


class AvailableGeographySerializer(ModelSerializer):
    """
    Serializer for the AvailableGeography model.
    """

    class Meta:
        model = Geography
        fields = ["name", "display_name"]
