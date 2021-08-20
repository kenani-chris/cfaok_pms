# Generated by Django 3.2.4 on 2021-08-19 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cfao_kenya', '0025_alter_staff_staff_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='staff_grade',
            field=models.CharField(blank=True, choices=[('T1', 'T1'), ('T6', 'T6'), ('T4', 'T4'), ('T2', 'T2'), ('T5', 'T5'), ('T3', 'T3')], help_text='user grade', max_length=5),
        ),
    ]
