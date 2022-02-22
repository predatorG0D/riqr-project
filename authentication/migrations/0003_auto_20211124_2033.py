# Generated by Django 3.2.8 on 2021-11-24 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_google'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='access_google',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='google',
            field=models.CharField(blank=True, default='', max_length=30, null=True),
        ),
    ]
