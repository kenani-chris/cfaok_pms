# Generated by Django 3.2.4 on 2021-07-04 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfao_kenya', '0009_auto_20210606_1729'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bu_kpi',
            old_name='bu_kpi_pms_id',
            new_name='bu_kpi_pms',
        ),
        migrations.RenameField(
            model_name='bu_kpi',
            old_name='bu_kpi_bu_user',
            new_name='bu_kpi_user',
        ),
        migrations.AddField(
            model_name='bu_kpi',
            name='bu_kpi_criteria',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_company',
            field=models.CharField(blank=True, choices=[('cfao_kenya', 'cfao_kenya'), ('tamk', 'tamk'), ('tydia', 'tydia'), ('cfao_agri', 'cfao_agri'), ('toyota_kenya', 'toyota_kenya')], help_text='user grade', max_length=15),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_grade',
            field=models.CharField(blank=True, choices=[('T2', 'T2'), ('T3', 'T3'), ('T4', 'T4'), ('T1', 'T1'), ('T6', 'T6'), ('T5', 'T5')], help_text='user grade', max_length=5),
        ),
    ]
