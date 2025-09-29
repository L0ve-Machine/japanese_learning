from django.urls import path
from . import views

app_name = 'translations'

urlpatterns = [
    path('translate/', views.translate_text, name='translate'),
    path('translate/batch/', views.translate_batch, name='translate_batch'),
    path('preference/', views.language_preference, name='language_preference'),
]