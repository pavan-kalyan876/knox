from django.urls import path
from .views import upload_csv
urlpatterns = [
    path('upload-csv/',upload_csv,name='upload-cdv'),
]
