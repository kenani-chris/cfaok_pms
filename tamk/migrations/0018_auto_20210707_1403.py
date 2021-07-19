# Generated by Django 3.2.4 on 2021-07-07 14:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cfao_kenya', '0017_auto_20210707_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='staff_company',
            field=models.CharField(blank=True, choices=[('cfao_kenya', 'cfao_kenya'), ('toyota_kenya', 'toyota_kenya'), ('cfao_agri', 'cfao_agri'), ('tamk', 'tamk'), ('tydia', 'tydia')], help_text='user grade', max_length=15),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_grade',
            field=models.CharField(blank=True, choices=[('T2', 'T2'), ('T1', 'T1'), ('T4', 'T4'), ('T5', 'T5'), ('T3', 'T3'), ('T6', 'T6')], help_text='user grade', max_length=5),
        ),
        migrations.CreateModel(
            name='kpi_months',
            fields=[
                ('kpi_months_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('kpi_month_april', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('kpi_month_may', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('kpi_month_june', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('kpi_month_july', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('kpi_month_august', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('kpi_month_september', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('kpi_month_october', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('kpi_month_november', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('kpi_month_december', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('kpi_month_january', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('kpi_month_february', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('kpi_month_march', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('kpi_months_pms', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='cfao_kenya.pms')),
            ],
        ),
    ]