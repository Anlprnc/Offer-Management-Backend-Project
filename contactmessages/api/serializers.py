from rest_framework import serializers
from contactmessages.models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'company', 'email', 'phone', 'message']