# coding: utf-8
from rest_framework import routers

from plates_app.views import NumberPlateViewSet

router = routers.DefaultRouter()
router.register(r'plates', NumberPlateViewSet)
