from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.cart.models import Cart, CartItem
from apps.products.models import Product
from apps.users.models import Address, User


class TestCheckoutApi(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='StrongPass123')
		self.token = Token.objects.create(user=self.user)
		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

		self.product = Product.objects.create(
			name='Keyboard',
			description='Mechanical keyboard',
			price='50.00',
			stock=10,
		)

		self.address = Address.objects.create(
			user=self.user,
			street='Main Street',
			city='amman',
			state='Amman',
			postal_code='11181',
			country='Jordan',
		)

		self.cart = Cart.objects.create(user=self.user, total_price='100.00')
		CartItem.objects.create(
			cart=self.cart,
			product=self.product,
			quantity=2,
			price_at_addition='50.00',
		)

	def test_checkout_creates_order_and_reduces_stock(self):
		response = self.client.post('/api/orders/checkout/', {'address_id': self.address.id}, format='json')

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.product.refresh_from_db()
		self.assertEqual(self.product.stock, 8)

	def test_checkout_fails_when_stock_is_insufficient(self):
		self.product.stock = 1
		self.product.save(update_fields=['stock'])

		response = self.client.post('/api/orders/checkout/', {'address_id': self.address.id}, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
