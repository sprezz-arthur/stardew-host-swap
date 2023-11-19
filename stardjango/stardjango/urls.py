from django.urls import path
from . import views

urlpatterns = [
    path("", views.editor, name="editor"),
    path("download/", views.download_file, name="download_file"),
]
