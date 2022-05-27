# Generated by Django 4.0.2 on 2022-05-26 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0010_translationgroup_alter_translation_translation_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translation',
            name='translation_group',
        ),
        migrations.AddField(
            model_name='translation',
            name='translation_group',
            field=models.ManyToManyField(to='learn.TranslationGroup'),
        ),
    ]
