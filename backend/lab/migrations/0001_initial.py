# Generated by Django 4.1.4 on 2022-12-12 21:14

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Chemical',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('name', models.CharField(max_length=255)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'DEVELOPER'), (1, 'STOP'), (2, 'FIXER'), (3, 'BLIX'), (4, 'STABILIZER')])),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.brand')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Development',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('name', models.CharField(max_length=255)),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'BN_NEGATIVE'), (1, 'BN_POSITIVE'), (2, 'COLOUR_NEGATIVE'), (3, 'COLOUR_POSITIVE')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1000)),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('temperature', models.IntegerField(default=20)),
                ('accuracy', models.IntegerField(default=0)),
                ('duration', models.DurationField(default=datetime.timedelta(seconds=600))),
                ('chemical', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.chemical')),
                ('development', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.development')),
            ],
            options={
                'unique_together': {('development', 'order')},
            },
        ),
    ]
