# Generated by Django 3.2.11 on 2022-05-19 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GraphQl', '0004_issue'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='description',
            new_name='detail',
        ),
    ]
