from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from vacations.models import Vacation, Like
from vacations.api.serializers.vacation_serializer import VacationSerializer, EditVacationSerializer, AddVacationSerializer
from django.db.models import Count
from typing import Any
from rest_framework.permissions import IsAdminUser



class VacationListView(APIView):
    """
    Returns a list of all vacations in the system,
    including like count and whether the current user liked each vacation.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        """
        Handle GET requests to retrieve all vacations.
        Adds 'like_count' and 'liked_by_user' to each vacation.
        """
        user_id: int = request.user.id
        vacations = Vacation.objects.all().order_by('start_date')

        serialized = VacationSerializer(vacations, many=True).data

        for vacation in serialized:
            vacation_id = vacation["id"]
            vacation["like_count"] = Like.objects.filter(vacation_id=vacation_id).count()
            vacation["liked_by_user"] = Like.objects.filter(
                vacation_id=vacation_id,
                user_id=user_id
            ).exists()

        return Response(serialized)
    
class AddVacationView(APIView):
    """
    API endpoint to add a new vacation (Admin only).
    """

    permission_classes = [IsAdminUser]

    def post(self, request) -> Response:
        """
        Handle POST request to add a vacation.
        """
        serializer: AddVacationSerializer = AddVacationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vacation added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EditVacationView(APIView):
    """
    API endpoint to edit an existing vacation (Admin only).
    """

    permission_classes = [IsAdminUser]

    def put(self, request, vacation_id: int) -> Response:
        """
        Handle PUT request to update a vacation.
        """
        try:
            vacation = Vacation.objects.get(id=vacation_id)
        except Vacation.DoesNotExist:
            return Response({"error": "Vacation not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer: EditVacationSerializer = EditVacationSerializer(vacation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vacation updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteVacationView(APIView):
    """
    API endpoint to delete a vacation (Admin only).
    """

    permission_classes = [IsAdminUser]

    def delete(self, request, vacation_id: int) -> Response:
        """
        Handle DELETE request to remove a vacation.
        """
        deleted, _ = Vacation.objects.filter(id=vacation_id).delete()

        if deleted == 0:
            return Response({"error": "Vacation not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Vacation deleted successfully."})
    
