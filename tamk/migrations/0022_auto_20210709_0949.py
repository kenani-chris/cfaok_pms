# Generated by Django 3.2.4 on 2021-07-09 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfao_kenya', '0021_auto_20210709_0639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='staff_company',
            field=models.CharField(blank=True, choices=[('cfao_kenya', 'cfao_kenya'), ('tydia', 'tydia'), ('toyota_kenya', 'toyota_kenya'), ('cfao_agri', 'cfao_agri'), ('tamk', 'tamk')], help_text='user grade', max_length=15),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_grade',
            field=models.CharField(blank=True, choices=[('T2', 'T2'), ('T6', 'T6'), ('T3', 'T3'), ('T4', 'T4'), ('T5', 'T5'), ('T1', 'T1')], help_text='user grade', max_length=5),
        ),
    ]
