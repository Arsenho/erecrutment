# Generated by Django 3.0.6 on 2020-06-18 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joboffer', '0002_auto_20200617_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='salary',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]