# Generated by Django 3.0.1 on 2020-04-25 22:28

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import rhymefind.models


class Migration(migrations.Migration):

    dependencies = [
        ('rhymefind', '0018_glove32dind_rhyme_pair_neighbors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='glove32dind',
            name='rhyme_pair_neighbors',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=rhymefind.models.rhyme_pair_neighbors_default),
        ),
    ]
