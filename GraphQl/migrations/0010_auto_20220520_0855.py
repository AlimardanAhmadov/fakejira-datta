# Generated by Django 3.2.11 on 2022-05-20 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GraphQl', '0009_flowtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='connector_loc',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='rect_loc',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
