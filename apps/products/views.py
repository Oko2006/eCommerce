from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
	serializer_class = ProductSerializer
	permission_classes = [AllowAny]

	def get_queryset(self):
		queryset = Product.objects.all().order_by('-created_at')
		search = self.request.query_params.get('q')
		if search:
			queryset = queryset.filter(name__icontains=search)
		return queryset
