# Generated by Django 3.2.3 on 2021-05-22 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cfao_kenya', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bu_kpi',
            name='bu_kpi_bu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_Bu_identity', to='cfao_kenya.bu'),
        ),
        migrations.AlterField(
            model_name='bu_kpi',
            name='bu_kpi_bu_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_Bu_submitting', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bu_kpi',
            name='bu_kpi_team_leader_approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_bu_team_leader_approval', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='checkIn_staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_individual_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='checkIn_team_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_team_leader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='company_kpi',
            name='company_kpi_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_person_submitting', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='done_staff_evaluates_tl',
            name='done_q1',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q1', to='cfao_kenya.question_staff_evaluate_tl'),
        ),
        migrations.AlterField(
            model_name='done_staff_evaluates_tl',
            name='done_q2',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q2', to='cfao_kenya.question_staff_evaluate_tl'),
        ),
        migrations.AlterField(
            model_name='done_staff_evaluates_tl',
            name='done_q3',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q3', to='cfao_kenya.question_staff_evaluate_tl'),
        ),
        migrations.AlterField(
            model_name='done_staff_evaluates_tl',
            name='done_q4',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q4', to='cfao_kenya.question_staff_evaluate_tl'),
        ),
        migrations.AlterField(
            model_name='done_staff_evaluates_tl',
            name='done_q5',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q5', to='cfao_kenya.question_staff_evaluate_tl'),
        ),
        migrations.AlterField(
            model_name='done_staff_evaluates_tl',
            name='done_q6',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q6', to='cfao_kenya.question_staff_evaluate_tl'),
        ),
        migrations.AlterField(
            model_name='done_staff_evaluates_tl',
            name='done_q7',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q7', to='cfao_kenya.question_staff_evaluate_tl'),
        ),
        migrations.AlterField(
            model_name='done_staff_evaluates_tl',
            name='done_staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_staff_evaluating', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='done_staff_evaluates_tl',
            name='done_team_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_tl_evaluated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='done_tl_evaluates_staff',
            name='done_q1',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q1', to='cfao_kenya.question_tl_evaluate_staff'),
        ),
        migrations.AlterField(
            model_name='done_tl_evaluates_staff',
            name='done_q2',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q2', to='cfao_kenya.question_tl_evaluate_staff'),
        ),
        migrations.AlterField(
            model_name='done_tl_evaluates_staff',
            name='done_q3',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q3', to='cfao_kenya.question_tl_evaluate_staff'),
        ),
        migrations.AlterField(
            model_name='done_tl_evaluates_staff',
            name='done_q4',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q4', to='cfao_kenya.question_tl_evaluate_staff'),
        ),
        migrations.AlterField(
            model_name='done_tl_evaluates_staff',
            name='done_q5',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q5', to='cfao_kenya.question_tl_evaluate_staff'),
        ),
        migrations.AlterField(
            model_name='done_tl_evaluates_staff',
            name='done_q6',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q6', to='cfao_kenya.question_tl_evaluate_staff'),
        ),
        migrations.AlterField(
            model_name='done_tl_evaluates_staff',
            name='done_q7',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_q7', to='cfao_kenya.question_tl_evaluate_staff'),
        ),
        migrations.AlterField(
            model_name='done_tl_evaluates_staff',
            name='done_staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_staff_evaluated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='done_tl_evaluates_staff',
            name='done_team_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_tl_evaluating', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='individual_kpi',
            name='individual_kpi_bu_leader_approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_bu_leader_approval', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='individual_kpi',
            name='individual_kpi_team_leader_approval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_team_leader_approval', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='individual_kpi',
            name='individual_kpi_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_user_submitting', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_notification_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_notification_Sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='responses_staff_evaluate_tl',
            name='response_staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_responding_staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='responses_staff_evaluate_tl',
            name='response_team_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_responded_team_leader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='responses_tl_evaluate_staff',
            name='response_staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_responded_staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='responses_tl_evaluate_staff',
            name='response_team_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_responding_team_leader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_belongs_to_branch', to='cfao_kenya.branch'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_bu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_belongs_to_bu', to='cfao_kenya.bu'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_company',
            field=models.CharField(blank=True, choices=[('cfao_agri', 'cfao_agri'), ('cfao_kenya', 'cfao_kenya'), ('toyota_kenya', 'toyota_kenya'), ('tydia', 'tydia'), ('tamk', 'tamk')], help_text='user grade', max_length=15),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_belongs_to_dept', to='cfao_kenya.department'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_grade',
            field=models.CharField(blank=True, choices=[('T6', 'T6'), ('T2', 'T2'), ('T1', 'T1'), ('T4', 'T4'), ('T5', 'T5'), ('T3', 'T3')], help_text='user grade', max_length=5),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_head_branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_is_head_branch', to='cfao_kenya.branch'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_head_bu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_is_head_bu', to='cfao_kenya.bu'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_head_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_is_head_dept', to='cfao_kenya.department'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_head_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_is_head_team', to='cfao_kenya.team'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cfao_kenya_staff_person', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='cfao_kenya_belongs_to_team', to='cfao_kenya.team'),
        ),
    ]
