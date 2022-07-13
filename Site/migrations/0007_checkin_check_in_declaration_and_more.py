# Generated by Django 4.0.3 on 2022-07-07 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0006_staff_staff_bu_override'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='check_in_declaration',
            field=models.TextField(default=None),
        ),
        '''migrations.AddField(
            model_name='submissioncheckin',
            name='submission_maximum_score_override',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='submissioncheckin',
            name='submission_minimum_score_override',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='submissioncheckin',
            name='submission_zero_results',
            field=models.IntegerField(default=0),
        ),''',
        migrations.AlterField(
            model_name='checkin',
            name='check_in_performance_area',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='check_in_progress_discussed',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='check_in_team_leader_support',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='check_in_team_member_actions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='kpitype',
            name='type_kpi',
            field=models.CharField(choices=[('Annual Target', 'Annual Target'), ('Monthly Target', 'Monthly Target'), ('BSC - Monthly Target', 'BSC'), ('BSC - Annual Target', 'BSC1')], default='Annual Target', max_length=20),
        ),
    ]
