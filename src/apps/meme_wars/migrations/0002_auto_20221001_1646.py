# Generated by Django 3.2.9 on 2022-10-01 16:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme_wars', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='war',
            name='has_ended',
        ),
        migrations.RemoveField(
            model_name='war',
            name='is_published',
        ),
        migrations.AddField(
            model_name='war',
            name='phase',
            field=models.CharField(choices=[('preparation', 'preparation'), ('submission', 'submission'), ('voting', 'voting'), ('finished', 'finished')], default='preparation', max_length=12, verbose_name='phase'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='score',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='score'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='VotingScore',
        ),
    ]
