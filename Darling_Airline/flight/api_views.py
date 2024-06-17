from rest_framework import status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.decorators import api_view # type: ignore
from django.contrib.auth.hashers import check_password, check_password
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import User
from .serializers import UserSerializer

@api_view(['POST'])
@ensure_csrf_cookie
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Account created successfully! Please log in."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@ensure_csrf_cookie
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            # Simulating manual session creation
            request.session['user_id'] = user.user_id
            request.session['username'] = user.username
            return Response({"detail": f"Welcome {username}!"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Wrong Username or Password!"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"detail": "Wrong Username or Password!"}, status=status.HTTP_401_UNAUTHORIZED)