# Generated by Django 3.1.2 on 2020-11-23 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0001_initial'),
        ('students', '0003_auto_20201013_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teachers.teacher'),
        ),
    ]