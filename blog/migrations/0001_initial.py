# Generated by Django 2.2.4 on 2019-08-11 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crawler_Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ptag', models.CharField(max_length=1000)),
                ('ntag', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Crawler_Tables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ptag', models.CharField(max_length=1000)),
                ('ntag', models.CharField(max_length=1000)),
                ('ttlfeed', models.CharField(max_length=30)),
                ('crwfeed', models.CharField(max_length=30)),
                ('succnt', models.CharField(max_length=10)),
                ('failcnt', models.CharField(max_length=10)),
                ('created_at', models.CharField(max_length=20)),
                ('updated_at', models.DateTimeField(max_length=20)),
                ('working_while', models.DateTimeField(max_length=20)),
                ('filename', models.CharField(max_length=20)),
            ],
        ),
    ]