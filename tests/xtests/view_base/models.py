from django.db import models


class ModelA(models.Model):
    name = models.CharField(max_length=64)


class ModelB(models.Model):
    name = models.CharField(max_length=64)


class ModelPrimary(models.Model):
    name = models.CharField(max_length=10)


class ModelSecondary(models.Model):
    name = models.CharField(max_length=10)
    related = models.ForeignKey(ModelPrimary)
