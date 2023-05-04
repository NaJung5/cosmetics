import json
from django.db import transaction
from rest_framework import permissions
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from .models import brand_category
from .serializers import BrandCategorySerializer
from datetime import datetime


class TestView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(tags=['brandCategoryInsert'], request_body=BrandCategorySerializer)
    @transaction.atomic
    def post(self, request):
        now = datetime.now()
        data = json.loads(request.body)
        site_depth3 = data.get('site_depth3', None)

        brand_category.objects.create(
            brand_type=data['brand_type'],
            site_depth1=data['site_depth1'],
            site_depth2=data['site_depth2'],
            site_depth3=site_depth3,
            depth1=data['depth1'],
            depth2=data['depth2'],
            reg_date=now
        )
        return JsonResponse({'message': 'CREATE_SUCCESS'}, status=200)
