from rest_framework import routers
from .views import PaymentView

routers = routers.DefaultRouter()

routers.register(r'', PaymentView, basename='payment')

urlpatterns = routers.urls