from rest_framework import serializers


class BrandCategorySerializer(serializers.Serializer):
    brand_type = serializers.CharField(help_text='사이트명', required=True)
    site_depth1 = serializers.CharField(help_text='대카테고리', required=True)
    site_depth2 = serializers.CharField(help_text='중카테고리', required=True)
    site_depth3 = serializers.CharField(help_text='소카테고리', required=False, allow_null=True, allow_blank=True)
    depth1 = serializers.CharField(help_text='대카테고리코드', required=True)
    depth2 = serializers.CharField(help_text='중카테고리코드', required=True)
