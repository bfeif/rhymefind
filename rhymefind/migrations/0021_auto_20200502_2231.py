# Generated by Django 3.0.1 on 2020-05-02 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rhymefind', '0020_rhymefind_find_distance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rhymecouplet',
            old_name='glove',
            new_name='glove_mean',
        ),
    ]
