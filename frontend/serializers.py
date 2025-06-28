from rest_framework import serializers
from .models import Vacation, Country, User

class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
