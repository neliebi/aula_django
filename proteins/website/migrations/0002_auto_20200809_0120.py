# Generated by Django 2.2.15 on 2020-08-09 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geneontology',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
