# Generated by Django 4.1.1 on 2022-09-15 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppleStore',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('track_name', models.TextField(blank=True, null=True)),
                ('n_citacoes', models.BigIntegerField(blank=True, default=0, null=True)),
                ('size_bytes', models.BigIntegerField(blank=True, null=True)),
                ('price', models.TextField(blank=True, null=True)),
                ('prime_genre', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
