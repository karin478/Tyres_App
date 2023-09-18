from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views



router = DefaultRouter()
# Register viewsets with the router
router.register(r'weekend_format', views.WeekendFormatViewSet)
router.register(r'weekend_session', views.WeekendSessionViewSet)
router.register(r'tyre_sets', views.TyreSetViewSet)
router.register(r'weekend_template', views.WeekendTemplateViewSet)



urlpatterns = [
    path('api/', include(router.urls)),



]
