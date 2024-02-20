from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()
