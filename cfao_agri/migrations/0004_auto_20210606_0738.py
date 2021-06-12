# Generated by Django 3.2.3 on 2021-06-06 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfao_agri', '0003_auto_20210522_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='staff_company',
            field=models.CharField(blank=True, choices=[('tamk', 'tamk'), ('cfao_agri', 'cfao_agri'), ('cfao_kenya', 'cfao_kenya'), ('tydia', 'tydia'), ('toyota_kenya', 'toyota_kenya')], help_text='user grade', max_length=15),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_grade',
            field=models.CharField(blank=True, choices=[('T1', 'T1'), ('T2', 'T2'), ('T3', 'T3'), ('T5', 'T5'), ('T6', 'T6'), ('T4', 'T4')], help_text='user grade', max_length=5),
        ),
    ]
