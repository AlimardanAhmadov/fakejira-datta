# Generated by Django 3.2.11 on 2022-05-19 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GraphQl', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(blank=True, max_length=50, null=True)),
                ('label', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
