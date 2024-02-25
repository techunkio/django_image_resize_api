from rest_framework import serializers


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    # width_cm = serializers.FloatField(required=False)
    # height_cm = serializers.FloatField(required=False)
    width_px = serializers.IntegerField(required=False)
    height_px = serializers.IntegerField(required=False)
    # filename = serializers.CharField(required=False)
    format = serializers.CharField(required=False)
    # crop_left = serializers.IntegerField(required=False)
    # crop_top = serializers.IntegerField(required=False)
    # crop_right = serializers.IntegerField(required=False)
    # crop_bottom = serializers.IntegerField(required=False)

    def validate(self, data):
        if 'format' in data:
            image_format = data['format']
            if image_format.lower() == 'jpg' or image_format.lower() == 'jpeg':
                data['format'] = 'JPEG'
            elif image_format.lower() == 'png':
                data['format'] = 'PNG'
        return data
