# Generated by Django 2.2.3 on 2019-11-01 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0008_auto_20190720_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='room',
            field=models.CharField(db_index=True, help_text='Аудитория где проходят занятия.', max_length=50, verbose_name='аудитория'),
        ),
    ]
