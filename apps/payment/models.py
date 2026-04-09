from django.db import models


class Payment(models.Model):
	STATUS_PENDING = 'pending'
	STATUS_SUCCESS = 'success'
	STATUS_FAILED = 'failed'

	STATUS_CHOICES = [
		(STATUS_PENDING, 'Pending'),
		(STATUS_SUCCESS, 'Success'),
		(STATUS_FAILED, 'Failed'),
	]

	PROVIDER_COD = 'cod'
	PROVIDER_MOCK = 'mock_gateway'

	PROVIDER_CHOICES = [
		(PROVIDER_COD, 'Cash On Delivery'),
		(PROVIDER_MOCK, 'Mock Gateway'),
	]

	order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='payment')
	provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default=PROVIDER_COD)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	transaction_id = models.CharField(max_length=255, blank=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	currency = models.CharField(max_length=10, default='JOD')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'Payment for order #{self.order_id} ({self.status})'
