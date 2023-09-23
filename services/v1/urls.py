from api.v1.views import GroomerViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("groomer", GroomerViewSet)

urlpatterns = router.urls
