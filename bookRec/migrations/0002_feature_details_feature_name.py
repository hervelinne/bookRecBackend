# Generated by Django 4.1.3 on 2023-11-05 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookRec', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='details',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='feature',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
