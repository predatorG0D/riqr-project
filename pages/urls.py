from django.urls import path

from .views import (
    GetUserPagesAPIView, PageAPIView, FilesAPIView, NationalitiesAPIView, PromocodeAPIView
)

app_name = 'pages'

urlpatterns = [
    path('user/pages/', GetUserPagesAPIView.as_view()),
    path('page/', PageAPIView.as_view()),
    path('files/', FilesAPIView.as_view()),
    path('nationalities/', NationalitiesAPIView.as_view()),
    path('promocode/', PromocodeAPIView.as_view()),
]
