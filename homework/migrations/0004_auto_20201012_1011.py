# Generated by Django 3.1.2 on 2020-10-12 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0001_initial'),
        ('homework', '0003_auto_20201012_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers.teacher'),
        ),
    ]
