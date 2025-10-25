from rest_framework import routers
from .views import CartItemViewSet

router = routers.DefaultRouter()
router.register(r'cart', CartItemViewSet, basename='cart')

urlpatterns = router.urls
