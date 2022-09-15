from django.db import models

class AppleStore(models.Model):
    id = models.BigIntegerField(primary_key=True)
    track_name = models.TextField(blank=True, null=True)
    n_citacoes = models.BigIntegerField(blank=True, null=True, default=0)
    size_bytes = models.BigIntegerField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    prime_genre = models.TextField(blank=True, null=True)