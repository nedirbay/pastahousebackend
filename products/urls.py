from rest_framework import routers
from .views import ProductViewSet, CategoryViewSet, TagViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = router.urls
