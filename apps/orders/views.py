from django.db import transaction
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.cart.models import Cart
from apps.users.models import Address
from .models import Order, OrderItem
from .serializers import CheckoutSerializer, OrderSerializer


class OrderListView(generics.ListAPIView):
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Order.objects.filter(user=self.request.user).order_by('-placed_at')


class OrderDetailView(generics.RetrieveAPIView):
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Order.objects.filter(user=self.request.user)


class CheckoutView(APIView):
	permission_classes = [IsAuthenticated]

	@transaction.atomic
	def post(self, request):
		serializer = CheckoutSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		user = request.user
		address_id = serializer.validated_data['address_id']

		try:
			address = Address.objects.get(id=address_id, user=user)
		except Address.DoesNotExist:
			return Response({'detail': 'Address not found.'}, status=status.HTTP_404_NOT_FOUND)

		try:
			cart = Cart.objects.select_for_update().get(user=user)
		except Cart.DoesNotExist:
			return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

		cart_items = list(cart.cartitem_set.select_related('product').all())
		if not cart_items:
			return Response({'detail': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

		for item in cart_items:
			if item.quantity > item.product.stock:
				return Response(
					{'detail': f'Not enough stock for product "{item.product.name}".'},
					status=status.HTTP_400_BAD_REQUEST,
				)

		order = Order.objects.create(
			user=user,
			address=address,
			cart=cart,
			total_price=cart.total_price,
		)

		for item in cart_items:
			OrderItem.objects.create(
				order=order,
				product=item.product,
				product_name=item.product.name,
				quantity=item.quantity,
				price=item.price_at_addition,
			)
			item.product.stock -= item.quantity
			item.product.save(update_fields=['stock'])

		cart.cartitem_set.all().delete()
		cart.total_price = 0
		cart.save(update_fields=['total_price', 'updated_at'])

		return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
