from django.urls import path
from imageresizer import views

urlpatterns = [
    path('resizeimage/', views.ResizeImageView.as_view(), name='resizeimage'),
]
