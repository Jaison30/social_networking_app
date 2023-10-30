# authentication/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserLoginSerializer
from .models import CustomUser


User = get_user_model()


class UserLoginView(APIView):
    """
    View for User Login.

    Args:
        email (str): email of the user.
        password (str): password of the user.

    Returns:
        Response: User token, status 200.
    """
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']            
            try:
                user = CustomUser.objects.get(email__iexact=email)
            except CustomUser.DoesNotExist:
                return Response({'error': 'User DoesNotExist'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserCreateView(generics.CreateAPIView):
    """
    View for User Signup.

    Args:
        username (str): username of the user
        email (str): email of the user.
        password (str): password of the user.

    Returns:
        Response: User token, status 201.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    View for User Logout.

    Args:
        token (str): token of the user

    Returns:
        Response: status 200.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)
