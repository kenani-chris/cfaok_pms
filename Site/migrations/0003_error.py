# Generated by Django 4.0.2 on 2022-02-21 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Site', '0002_alter_staff_staff_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('error_id', models.AutoField(primary_key=True, serialize=False)),
                ('error_title', models.CharField(max_length=50)),
                ('error_description', models.TextField()),
                ('error_resoltion', models.TextField()),
            ],
        ),
    ]