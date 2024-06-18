from django.shortcuts import render
from django.http import HttpResponse
# import cv2 as cv
# import numpy as np
import base64
def index(request):

    if request.method == "POST":
        # image = request.FILES.get("image-uploaded")
        # image_data = image.read()
        # nparr = np.frombuffer(image_data, np.uint8)
        # image_read = cv.imdecode(nparr, cv.IMREAD_COLOR)
        # h, w = image_read.shape[:2]
        # encoded_image = cv.imencode(".jpg", image_read)
        # base_64_encoded = base64.b64encode(encoded_image)
        return HttpResponse("base_64_encoded")
    else:
        context ={
            "user": request.user,
        }
        return render(request, 'vision/vision.html', context)
