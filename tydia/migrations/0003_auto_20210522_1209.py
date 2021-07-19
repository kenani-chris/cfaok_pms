# Generated by Django 3.2.3 on 2021-05-22 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfao_kenya', '0002_auto_20210522_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='staff_company',
            field=models.CharField(blank=True, choices=[('tamk', 'tamk'), ('cfao_agri', 'cfao_agri'), ('tydia', 'tydia'), ('cfao_kenya', 'cfao_kenya'), ('toyota_kenya', 'toyota_kenya')], help_text='user grade', max_length=15),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_grade',
            field=models.CharField(blank=True, choices=[('T1', 'T1'), ('T3', 'T3'), ('T2', 'T2'), ('T4', 'T4'), ('T6', 'T6'), ('T5', 'T5')], help_text='user grade', max_length=5),
        ),
    ]
