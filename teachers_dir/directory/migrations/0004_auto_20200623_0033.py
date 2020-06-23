# Generated by Django 3.0.7 on 2020-06-22 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0003_auto_20200622_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='Email_Address',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='First_Name',
            field=models.CharField(max_length=60, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='Last_Name',
            field=models.CharField(max_length=60, verbose_name='Last Name'),
        ),
    ]