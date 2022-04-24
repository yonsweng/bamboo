'''
User views
'''

from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def users(request):
    '''
    Create a user
    '''

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
# pylint: disable=too-many-return-statements
def user(request, user_id):
    '''
    GET: view the user's information
    PUT: edit the user's information
    DELETE: delete the user's information
    '''

    if not request.user.is_superuser and request.user.id != user_id:
        return JsonResponse({'error': 'Accesssing different user'})

    try:
        user_obj = UserSerializer.Meta.model.objects.get(id=user_id)
    except UserSerializer.Meta.model.DoesNotExist:
        return JsonResponse({'error': 'No user'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user_obj)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'PUT':
        serializer = UserSerializer(user_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        user_obj.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    return JsonResponse({'error': 'Method not allowed'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login(request):
    '''
    Login
    '''

    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)

    authenticated_user = authenticate(request, username=username, password=password)

    if not authenticated_user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=authenticated_user)

    return Response({'token': token.key}, status=status.HTTP_200_OK)
