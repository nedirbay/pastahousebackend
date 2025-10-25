from rest_framework import viewsets, permissions, filters
from .models import Product, Category, Tag, Review
from .serializers import ProductSerializer, CategorySerializer, TagSerializer, ReviewSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name', 'tags__name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def latest(self, request):
        """Return latest products. Query param: count (default 5)."""
        try:
            count = int(request.query_params.get('count', 5))
        except (ValueError, TypeError):
            count = 5
        products = Product.objects.all().order_by('-created_at')[:max(0, count)]
        serializer = self.get_serializer(products, many=True)
        return Response({'count': len(serializer.data), 'products': serializer.data})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
