from .serializers import TODOSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import TODOSerializer,UserSerializer
from .models import TODO
from django.views.decorators.cache import cache_page


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  # Apply the custom throttle
def todo_list(request):
    user = request.user
    todos = TODO.objects.filter(user=user).order_by('priority')
    serializer = TODOSerializer(todos, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  # Apply the custom throttle
def create_todo(request):
    serializer = TODOSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_todo(request, id):
    try:
        todo = TODO.objects.get(pk=id)
    except TODO.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if todo.user != request.user:
        return Response({'message': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)

    todo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_todo_status(request, id, status):
    try:
        todo = TODO.objects.get(pk=id)
    except TODO.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if todo.user != request.user:
        return Response({'message': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)

    todo.status = status
    todo.save()
    return Response({'message': 'Status updated successfully'}, status=status.HTTP_200_OK)


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .serializers import TODOSerializer
from .models import TODO

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.auth.delete()
    return Response(status=status.HTTP_200_OK)

# TODO views (Create, Read, Update, Delete)
