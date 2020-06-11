# Generated by Django 3.0.6 on 2020-06-05 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('joboffer', '0001_initial'),
        ('registration', '0001_initial'),
        ('evaluation', '0002_auto_20200605_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='applicants',
            field=models.ManyToManyField(related_name='candidates_applying_for_offer', through='joboffer.Apply', to='registration.Candidate'),
        ),
        migrations.AddField(
            model_name='offer',
            name='published_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employer_created_offer', to='registration.Employer'),
        ),
        migrations.AddField(
            model_name='offer',
            name='tests',
            field=models.ManyToManyField(blank=True, to='evaluation.Test'),
        ),
        migrations.AddField(
            model_name='apply',
            name='candidate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.Candidate'),
        ),
        migrations.AddField(
            model_name='apply',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='joboffer.Offer'),
        ),
    ]