# Generated by Django 4.0.1 on 2022-02-02 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('local', '0006_user_table_address_user_table_messageonoff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='imageURL',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='userID',
        ),
    ]
