from rest_framework import viewsets
from vacations.models import Vacation, Country, User, Like
from frontend.serializers import VacationSerializer, CountrySerializer, UserSerializer, LikeSerializer


class VacationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows vacations to be viewed or edited.
    """
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer


class CountryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows countries to be viewed or edited.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LikeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows likes to be viewed or edited.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
