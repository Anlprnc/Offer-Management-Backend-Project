from django.urls import path
from .views import ContactMessageView

urlpatterns = [
    path('contact-message/', ContactMessageView.as_view(), name='contact-message'),
]
