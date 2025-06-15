from rest_framework.routers import DefaultRouter

from .views import PetViewSet

router = DefaultRouter()
router.register(r"", PetViewSet, basename="pet")

urlpatterns = router.urls
