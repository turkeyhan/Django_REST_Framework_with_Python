# Generated by Django 3.2.10 on 2023-08-21 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='catecory',
            new_name='category',
        ),
    ]