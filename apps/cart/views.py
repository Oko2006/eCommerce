from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product

from .models import Cart, CartItem
from .serializers import AddCartItemSerializer, CartSerializer, UpdateCartItemSerializer


def get_user_cart(user):
	cart, _ = Cart.objects.get_or_create(user=user)
	return cart


def recalculate_cart_total(cart):
	total = Decimal('0.00')
	for item in cart.cartitem_set.select_related('product').all():
		total += item.price_at_addition * item.quantity
	cart.total_price = total
	cart.save(update_fields=['total_price', 'updated_at'])


class CartView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		cart = get_user_cart(request.user)
		serializer = CartSerializer(cart)
		return Response(serializer.data)


class CartItemCreateView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = AddCartItemSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		cart = get_user_cart(request.user)
		try:
			product = Product.objects.get(id=serializer.validated_data['product_id'])
		except Product.DoesNotExist:
			return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
		quantity = serializer.validated_data['quantity']

		if quantity > product.stock:
			return Response({'detail': 'Requested quantity exceeds stock.'}, status=status.HTTP_400_BAD_REQUEST)

		item, created = CartItem.objects.get_or_create(
			cart=cart,
			product=product,
			defaults={
				'quantity': quantity,
				'price_at_addition': product.price,
			},
		)

		if not created:
			new_quantity = item.quantity + quantity
			if new_quantity > product.stock:
				return Response({'detail': 'Requested quantity exceeds stock.'}, status=status.HTTP_400_BAD_REQUEST)
			item.quantity = new_quantity
			item.save(update_fields=['quantity'])

		recalculate_cart_total(cart)
		return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
	permission_classes = [IsAuthenticated]

	def patch(self, request, item_id):
		serializer = UpdateCartItemSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		cart = get_user_cart(request.user)
		try:
			item = cart.cartitem_set.select_related('product').get(id=item_id)
		except CartItem.DoesNotExist:
			return Response({'detail': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

		quantity = serializer.validated_data['quantity']
		if quantity > item.product.stock:
			return Response({'detail': 'Requested quantity exceeds stock.'}, status=status.HTTP_400_BAD_REQUEST)

		item.quantity = quantity
		item.save(update_fields=['quantity'])
		recalculate_cart_total(cart)
		return Response(CartSerializer(cart).data)

	def delete(self, request, item_id):
		cart = get_user_cart(request.user)
		deleted_count, _ = cart.cartitem_set.filter(id=item_id).delete()
		if not deleted_count:
			return Response({'detail': 'Cart item not found.'}, status=status.HTTP_404_NOT_FOUND)

		recalculate_cart_total(cart)
		return Response(status=status.HTTP_204_NO_CONTENT)
