# Generated by Django 3.2.13 on 2022-04-29 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('lyric', models.CharField(max_length=65535)),
                ('genre', models.CharField(max_length=64)),
                ('release_date', models.DateField()),
                ('vector', models.CharField(max_length=65535)),
            ],
        ),
        migrations.AlterField(
            model_name='diary',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
