# Generated by Django 3.0.6 on 2020-06-18 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joboffer', '0003_auto_20200618_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='offer_category',
            field=models.CharField(blank=True, choices=[('it', 'IT'), ('hotelerie', 'Hotelerie'), ('enseignement', 'Enseignement'), ('immobilier', 'Immobilier'), ('finance', 'Finance'), ('medicale', 'Medicale'), ('ingenieurie', 'Ingenieurie')], max_length=32, null=True),
        ),
    ]
