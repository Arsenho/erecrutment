# Generated by Django 3.0.6 on 2020-06-05 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '0001_initial'),
        ('evaluation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.Employer'),
        ),
        migrations.AddField(
            model_name='test',
            name='participants',
            field=models.ManyToManyField(blank=True, through='evaluation.Participate', to='registration.Candidate'),
        ),
        migrations.AddField(
            model_name='test',
            name='questions',
            field=models.ManyToManyField(to='evaluation.Question'),
        ),
        migrations.AddField(
            model_name='solution',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.Employer'),
        ),
        migrations.AddField(
            model_name='solution',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='evaluation.Question'),
        ),
        migrations.AddField(
            model_name='question',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.Employer'),
        ),
        migrations.AddField(
            model_name='participate',
            name='candidate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='registration.Candidate'),
        ),
        migrations.AddField(
            model_name='participate',
            name='test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='evaluation.Test'),
        ),
    ]
