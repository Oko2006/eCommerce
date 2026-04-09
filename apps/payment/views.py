from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orders.models import Order

from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
	serializer_class = PaymentSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Payment.objects.filter(order__user=self.request.user).order_by('-created_at')

	def create(self, request, *args, **kwargs):
		order_id = request.data.get('order')
		if not order_id:
			return Response({'detail': 'Order is required.'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			order = Order.objects.get(id=order_id, user=request.user)
		except Order.DoesNotExist:
			return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

		if hasattr(order, 'payment'):
			return Response({'detail': 'Payment already exists for this order.'}, status=status.HTTP_400_BAD_REQUEST)

		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(order=order, amount=order.total_price)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	@action(detail=True, methods=['patch'])
	def mark_success(self, request, pk=None):
		payment = self.get_object()
		payment.status = Payment.STATUS_SUCCESS
		payment.transaction_id = request.data.get('transaction_id', payment.transaction_id)
		payment.save(update_fields=['status', 'transaction_id', 'updated_at'])
		return Response(self.get_serializer(payment).data)

	@action(detail=True, methods=['patch'])
	def mark_failed(self, request, pk=None):
		payment = self.get_object()
		payment.status = Payment.STATUS_FAILED
		payment.transaction_id = request.data.get('transaction_id', payment.transaction_id)
		payment.save(update_fields=['status', 'transaction_id', 'updated_at'])
		return Response(self.get_serializer(payment).data)
