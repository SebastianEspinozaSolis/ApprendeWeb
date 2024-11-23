from django.urls import path, include

app_name = 'ajustes'

urlpatterns = [
    path('', include('ajustes.urls')),
]
