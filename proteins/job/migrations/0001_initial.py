# Generated by Django 2.2.15 on 2020-10-09 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(max_length=20, unique=True)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]
