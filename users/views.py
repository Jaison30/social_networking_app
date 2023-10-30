from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from authentication.models import CustomUser 
from .serializers import UserSearchSerializer
from .serializers import UserSerializer
from .models import Friendship
from .serializers import FriendshipSerializer, FriendRequestStatusSerializer, FriendRequestSerializer
from .rate_limit import FriendRequestRateThrottle


class UserSearchAPIView(APIView):
    """
    View for search other users by email or name.

    Method:
        POST

    Args:
        email (str): email of the user.
        or
        name (str): name of the user.

    Returns:
        Response:  list of users, status 200.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        search_query = request.data.get('search_query', None)

        if search_query is None:
            return Response({'error': 'Username or email is required in the request data.'}, status=status.HTTP_404_NOT_FOUND)

        queryset = CustomUser.objects.filter(Q(username__icontains=search_query) | Q(email__icontains=search_query))
        serialized_queryset = UserSerializer(queryset, many=True)

        return Response(serialized_queryset.data, status=status.HTTP_200_OK)
    

class FriendRequestCreateView(generics.CreateAPIView):
    """
    View for send friend request.

    Method:
        POST

    Args:
        sender (pk): User id of the user.
        receiver (pk): User id of the user.
        
    Returns:
        Success:
            Response:  status 200.
        Failed:
            if user send more than 3 
            friend requests within a minute
            status code: 429 Too Many Requests
    """
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestRateThrottle]
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class FriendRequestAcceptView(generics.UpdateAPIView):
    """
    View for accept friend request.

    Method:
        PUT
    
    Args:
        (pk): Friendship id.

    Returns:
        Response:  status 200.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Friendship.objects.all()
    serializer_class = FriendRequestStatusSerializer

    def perform_update(self, serializer):
        serializer.save(status='accepted')


class FriendRequestRejectView(generics.UpdateAPIView):
    """
    View for reject friend request.

    Method:
        PUT
    
    Args:
        (pk): Friendship id.

    Returns:
        Response:  status 200.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Friendship.objects.all()
    serializer_class = FriendRequestStatusSerializer

    def perform_update(self, serializer):
        serializer.save(status='rejected')


class AcceptedFriendRequestListView(generics.ListAPIView):
    """
    View for get list of users who have accepted friend request.

    Method:
        GET
    
    Returns:
        Response: list of users,  status 200.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return Friendship.objects.filter(status='accepted', sender=self.request.user)
    

class PendingFriendRequestListView(generics.ListAPIView):
    """
    View for get list pending friend requests.

    Method:
        GET
    
    Returns:
        Response: list of users,  status 200.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return Friendship.objects.filter(status='pending', sender=self.request.user)