# Generated by Django 4.0.2 on 2022-05-16 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0005_alter_translation_translation_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translation',
            name='translation_key',
        ),
    ]
