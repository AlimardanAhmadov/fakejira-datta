# Generated by Django 3.2.11 on 2022-05-20 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GraphQl', '0008_auto_20220519_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlowType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('states', models.ManyToManyField(related_name='states', to='GraphQl.State')),
            ],
        ),
    ]
