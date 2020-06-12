# Generated by Django 3.0.6 on 2020-06-11 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('joboffer', '0005_auto_20200611_0852'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'permissions': [], 'verbose_name': 'Entreprise'},
        ),
        migrations.AlterField(
            model_name='offer',
            name='published_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employer_created_offer', to=settings.AUTH_USER_MODEL),
        ),
    ]
