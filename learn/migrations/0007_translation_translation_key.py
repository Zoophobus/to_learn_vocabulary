# Generated by Django 4.0.2 on 2022-05-16 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0006_remove_translation_translation_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='translation_key',
            field=models.CharField(default='<django.db.models.fields.related.ForeignKey> - <django.db.models.fields.related.ForeignKey>', max_length=203, unique=True),
        ),
    ]
