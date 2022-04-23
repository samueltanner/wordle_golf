from django.urls import include, path
from rest_framework import routers
from . import views

# router = routers.SimpleRouter()
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'scores', views.ScoreViewSet)
# router.register(r'scores_api', views.ScoreApiViewSet)
router.register(r'groups', views.GolfGroupViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]
