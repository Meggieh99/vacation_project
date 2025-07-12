from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from vacations.api.serializers.like_serializer import LikeActionSerializer
from rest_framework.authentication import SessionAuthentication
from vacations.models import Like


class LikeVacationView(APIView):
    """
    Add a like for a vacation by the authenticated user.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer: LikeActionSerializer = LikeActionSerializer(data=request.data)
        if serializer.is_valid():
            user_id: int = request.user.id
            vacation_id: int = serializer.validated_data["vacation_id"]

            if Like.objects.filter(user_id=user_id, vacation_id=vacation_id).exists():
                return Response({"error": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)

            Like.objects.create(user_id=user_id, vacation_id=vacation_id)
            return Response({"message": "Like added successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnlikeVacationView(APIView):
    """
    Remove a like for a vacation by the authenticated user.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        serializer: LikeActionSerializer = LikeActionSerializer(data=request.data)
        if serializer.is_valid():
            user_id: int = request.user.id
            vacation_id: int = serializer.validated_data["vacation_id"]

            deleted, _ = Like.objects.filter(user_id=user_id, vacation_id=vacation_id).delete()

            if deleted == 0:
                return Response({"error": "Like not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"message": "Like removed successfully"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
