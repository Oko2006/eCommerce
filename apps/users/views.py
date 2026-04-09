from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import Address
from .serializers import AddressSerializer, RegisterSerializer, UserSerializer


class RegisterView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		token, _ = Token.objects.get_or_create(user=user)
		return Response(
			{
				'token': token.key,
				'user': UserSerializer(user).data,
			},
			status=status.HTTP_201_CREATED,
		)


class LoginView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')
		user = authenticate(request, username=username, password=password)
		if not user:
			return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

		token, _ = Token.objects.get_or_create(user=user)
		return Response(
			{
				'token': token.key,
				'user': UserSerializer(user).data,
			}
		)


class ProfileView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		return Response(UserSerializer(request.user).data)


class AddressViewSet(viewsets.ModelViewSet):
	serializer_class = AddressSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Address.objects.filter(user=self.request.user).order_by('-id')

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)

	@action(detail=False, methods=['get'])
	def mine(self, request):
		serializer = self.get_serializer(self.get_queryset(), many=True)
		return Response(serializer.data)
