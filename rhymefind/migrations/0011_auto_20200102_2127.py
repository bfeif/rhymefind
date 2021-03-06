# Generated by Django 3.0.1 on 2020-01-02 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rhymefind', '0010_auto_20200102_2125'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='glove',
            name='rhymefind_g_word_6569b8_idx',
        ),
        migrations.RemoveIndex(
            model_name='rhymecouplet',
            name='rhymefind_r_word_1_29148c_idx',
        ),
        migrations.RemoveIndex(
            model_name='rhymecouplet',
            name='rhymefind_r_word_1_ebde88_idx',
        ),
        migrations.RemoveIndex(
            model_name='rhymecouplet',
            name='rhymefind_r_word_2_c7a677_idx',
        ),
        migrations.AddIndex(
            model_name='glove',
            index=models.Index(fields=['word'], name='Glove_word_idx'),
        ),
        migrations.AddIndex(
            model_name='rhymecouplet',
            index=models.Index(fields=['word_1', 'word_2'], name='Glove_word1_word2_idx'),
        ),
        migrations.AddIndex(
            model_name='rhymecouplet',
            index=models.Index(fields=['word_1'], name='Glove_word1_idx'),
        ),
        migrations.AddIndex(
            model_name='rhymecouplet',
            index=models.Index(fields=['word_2'], name='Glove_word2_idx'),
        ),
    ]
