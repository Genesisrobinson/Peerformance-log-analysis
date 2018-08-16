from rest_framework import serializers

from .models import List,card

class listserializer(serializers.ModelSerializer):
    class Meta:
        model=List
        fields = '__all__'

class cardserializer(serializers.ModelSerializer):
    class Meta:
        model=card
        fields = '__all__'
