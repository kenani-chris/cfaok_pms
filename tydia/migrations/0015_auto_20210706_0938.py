# Generated by Django 3.2.4 on 2021-07-06 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfao_kenya', '0014_auto_20210705_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='checkIn_month',
            field=models.CharField(default=None, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='checkIn_team_leader_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_company',
            field=models.CharField(blank=True, choices=[('cfao_kenya', 'cfao_kenya'), ('tydia', 'tydia'), ('cfao_agri', 'cfao_agri'), ('toyota_kenya', 'toyota_kenya'), ('tamk', 'tamk')], help_text='user grade', max_length=15),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_grade',
            field=models.CharField(blank=True, choices=[('T5', 'T5'), ('T3', 'T3'), ('T6', 'T6'), ('T4', 'T4'), ('T2', 'T2'), ('T1', 'T1')], help_text='user grade', max_length=5),
        ),
    ]
