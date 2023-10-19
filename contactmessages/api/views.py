from rest_framework.generics import CreateAPIView
from contactmessages.models import ContactMessage
from .serializers import ContactMessageSerializer
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status


class ContactMessageView(CreateAPIView):
    serializer_class = ContactMessageSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_Valid(raise_exception=True)
        self.perform_create(serializer)
        
        subject = 'New contact message'
        message = f'Name: {serializer.data["name"]}\nEmail: {serializer.data["email"]}\nPhone: {serializer.data["phone"]}\nMessage: {serializer.data["message"]}'
        
        if request.user.is_authenticated and request.user.email:
            from_email = request.user.email
        else:
            from_email = 'your_email@example.com'
            
        reciption_list = ['your_email@example.com']
        
        send_mail(subject, message, from_email, reciption_list, fail_silently=False)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)