# Generated by Django 5.1.7 on 2025-04-27 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title']},
        ),
        migrations.RenameField(
            model_name='book',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='book',
            name='summary',
            field=models.TextField(blank=True, help_text='Краткое описание книги', max_length=1000),
        ),
    ]
