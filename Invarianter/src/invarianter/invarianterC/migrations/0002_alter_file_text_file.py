# Generated by Django 3.2 on 2021-05-06 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invarianterC', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='text_file',
            field=models.FileField(upload_to='invarianterC/uploads/'),
        ),
    ]
