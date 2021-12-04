from django.urls import path

from . import views
from aiml_automate.views import upload_file,download_file,automate


urlpatterns = [
    path('',automate.as_view(), name='automate'),
    path('',upload_file.as_view(), name='upload'),
    path('',download_file.as_view(), name='download'),
]
