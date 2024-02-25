from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from PIL import Image
import io
from django.http import JsonResponse
from .serializer import ImageSerializer
import requests
import base64


class ResizeImageView(APIView):
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        print(serializer, "before ....................")
        if serializer.is_valid():
            print("inside valid function", serializer)
            image_data = serializer.validated_data['image'].read()
            # width_cm = serializer.validated_data.get('width_cm')
            # height_cm = serializer.validated_data.get('height_cm')
            width_px = serializer.validated_data.get('width_px')
            height_px = serializer.validated_data.get('height_px')

            # custom_filename = serializer.validated_data.get('filename')
            image_format = serializer.validated_data.get('format', 'JPEG')

            # crop_left = serializer.validated_data.get('crop_left')
            # crop_top = serializer.validated_data.get('crop_top')
            # crop_right = serializer.validated_data.get('crop_right')
            # crop_bottom = serializer.validated_data.get('crop_bottom')

            img = Image.open(io.BytesIO(image_data))
            print("image open", img)

            # if crop_left is not None and crop_top is not None and crop_right is not None and crop_bottom is not None:
            #     img = img.crop((crop_left, crop_top, crop_right, crop_bottom))

            if width_px and height_px:
                width_data = width_px
                height_data = height_px
            # elif width_cm and height_cm:
            #     width_data = int(width_cm * 37.7952755906)
            #     height_data = int(height_cm * 37.7952755906)
            else:
                return Response({"error": "Provide either pixel scale or centimeter scale for width and height"}, status=status.HTTP_400_BAD_REQUEST)

            resize_image = img.resize((width_data, height_data))
            print(resize_image, "resize image....")
            if resize_image.mode == 'RGBA':
                resize_image = resize_image.convert('RGB')

            output_stream = io.BytesIO()
            resize_image.save(output_stream, format=image_format, quality=90, optimize=True, progressive=True)
            print(resize_image, "After Save")
            output_stream.seek(0)
            print(output_stream, "output stream")
            try:
                base64_string = base64.b64encode(output_stream.getvalue()).decode('utf-8')
                print(base64_string, "base 64...output")
            except Exception as e:
                print(e, "Exception Error")

            url = 'https://api.imgur.com/3/image'

            data = {
                "image": base64_string,
                "type":  "base64",
                "title": "demo",
                "description": "demo"

            }

            token = '390fd1592441500'

            headers = {
               'Authorization': token
            }
            print('befor API call')

            try:
                response = requests.post(url, data=data, headers=headers)

                print("after api call", response.json())

                if response.status_code == 200:
                    response = JsonResponse(response.json(), safe=False)
                    response.content_type = 'application/json'
                    print(response)
                    return response
                # Print the response content

                else:
                    # If the request was not successful, print the error status code
                    print("API Error:", response.status_code)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            except Exception as e:
                print(e, 'Exception error')
