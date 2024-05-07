from django.db import models

# Create your models here.
class TestBulk(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)
    dept = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_bulk'


class TestBulk2(models.Model):
    dept_cd = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50, blank=True, null=True)
    pos = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_bulk2'