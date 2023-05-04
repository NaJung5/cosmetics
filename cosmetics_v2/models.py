from django.db import models


class brand_category(models.Model):
    sno = models.AutoField(primary_key=True)
    brand_type = models.CharField(max_length=5)
    site_depth1 = models.CharField(max_length=10)
    site_depth2 = models.CharField(max_length=10)
    site_depth3 = models.CharField(max_length=10)
    depth1 = models.CharField(max_length=5)
    depth2 = models.CharField(max_length=5)
    reg_date = models.DateTimeField()
    mod_date = models.DateTimeField()

    class Meta:
        app_label = 'cosmetics'
        db_table = 'brand_category'
