# Generated by Django 4.1.5 on 2023-01-21 05:32

import apps.wars.validators.meme_war_phase_validator
import apps.wars.validators.war_phase_validator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wars', '0004_alter_meme_image_alter_meme_war_alter_war_phase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meme',
            name='war',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='memes', to='wars.war', validators=[apps.wars.validators.war_phase_validator.WarPhaseValidator(phase_value='submission')], verbose_name='war'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='meme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='wars.meme', validators=[apps.wars.validators.meme_war_phase_validator.MemeWarPhaseValidator(phase_value='submission')], verbose_name='meme'),
        ),
    ]