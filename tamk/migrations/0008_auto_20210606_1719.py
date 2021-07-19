# Generated by Django 3.2.3 on 2021-06-06 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfao_kenya', '0007_auto_20210606_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='individual_kpi',
            name='individual_kpi_april_score_approve',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=13),
        ),
        migrations.AddField(
            model_name='individual_kpi',
            name='individual_kpi_august_score_approve',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=13),
        ),
        migrations.AddField(
            model_name='individual_kpi',
            name='individual_kpi_december_score_approve',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=13),
        ),
        migrations.AddField(
            model_name='individual_kpi',
            name='individual_kpi_february_score_approve',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=13),
        ),
        migrations.AddField(
            model_name='individual_kpi',
            name='individual_kpi_january_score_approve',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=13),
        ),
        migrations.AddField(
            model_name='individual_kpi',
            name='individual_kpi_july_score_approve',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=13),
        ),
        migrations.AddField(
            model_name='individual_kpi',
            name='individual_kpi_june_score_approve',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=13),
        ),
        migrations.AddField(
            model_name='individual_kpi',
            name='individual_kpi_march_score_approve',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=13),
        ),
        migrations.AddField(
            model_name='individual_kpi',
            name='individual_kpi_may_score_approve',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=13),
        ),
        migrations.AddField(
            model_name='individual_kpi',
            name='individual_kpi_november_score_approve',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=13),
        ),
        migrations.AddField(
            model_name='individual_kpi',
            name='individual_kpi_october_score_approve',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=13),
        ),
        migrations.AddField(
            model_name='individual_kpi',
            name='individual_kpi_september_score_approve',
            field=models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Not Approved', 'Not Approved')], default='Not Approved', max_length=13),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_company',
            field=models.CharField(blank=True, choices=[('toyota_kenya', 'toyota_kenya'), ('tydia', 'tydia'), ('tamk', 'tamk'), ('cfao_kenya', 'cfao_kenya'), ('cfao_agri', 'cfao_agri')], help_text='user grade', max_length=15),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_grade',
            field=models.CharField(blank=True, choices=[('T4', 'T4'), ('T5', 'T5'), ('T1', 'T1'), ('T2', 'T2'), ('T3', 'T3'), ('T6', 'T6')], help_text='user grade', max_length=5),
        ),
    ]
