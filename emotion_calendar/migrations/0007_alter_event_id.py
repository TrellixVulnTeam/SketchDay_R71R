# Generated by Django 3.2.13 on 2022-04-29 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emotion_calendar', '0006_auto_20220429_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
