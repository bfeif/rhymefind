# Generated by Django 3.0.1 on 2020-05-20 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rhymefind', '0037_word_num_finds'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rhymefind',
            unique_together={('word', 'rhyme_couplet')},
        ),
    ]
