# Generated by Django 4.0.1 on 2022-01-31 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('local', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gossip_table',
            name='imageURL',
            field=models.CharField(max_length=200),
        ),
    ]