# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='driver',
            fields=[
                ('driver_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='pickup_req',
            fields=[
                ('req_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted_at', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(max_length=1, default='W', choices=[('W', 'Waiting'), ('O', 'Ongoing'), ('C', 'Complete')])),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.customer')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.driver')),
            ],
        ),
    ]
