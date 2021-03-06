# Generated by Django 4.0.2 on 2022-05-22 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0009_translation_translation_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranslationGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupName', models.CharField(max_length=50, unique=True)),
                ('created', models.DateField(auto_now_add=True, verbose_name='Date')),
            ],
        ),
        migrations.AlterField(
            model_name='translation',
            name='translation_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='learn.translationgroup'),
        ),
    ]
