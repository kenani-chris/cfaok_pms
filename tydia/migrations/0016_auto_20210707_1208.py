# Generated by Django 3.2.4 on 2021-07-07 12:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cfao_kenya', '0015_auto_20210706_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='staff_grade',
            fields=[
                ('grade_id', models.UUIDField(default=uuid.uuid4, help_text='Unique identfier for staff grade', primary_key=True, serialize=False)),
                ('grade', models.CharField(blank=True, help_text='Staff Grade', max_length=10, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_company',
            field=models.CharField(blank=True, choices=[('cfao_kenya', 'cfao_kenya'), ('cfao_agri', 'cfao_agri'), ('toyota_kenya', 'toyota_kenya'), ('tydia', 'tydia'), ('tamk', 'tamk')], help_text='user grade', max_length=15),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_grade',
            field=models.CharField(blank=True, choices=[('T5', 'T5'), ('T3', 'T3'), ('T6', 'T6'), ('T1', 'T1'), ('T4', 'T4'), ('T2', 'T2')], help_text='user grade', max_length=5),
        ),
        migrations.AddField(
            model_name='score_matrix',
            name='matrix_grade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='cfao_kenya.staff_grade'),
        ),
    ]