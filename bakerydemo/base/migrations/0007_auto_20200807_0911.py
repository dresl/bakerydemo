# Generated by Django 3.0.9 on 2020-08-07 09:11

from django.db import migrations
import djrichtextfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_standardpage_body_rich'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standardpage',
            name='body_rich',
            field=djrichtextfield.models.RichTextField(blank=True, null=True),
        ),
    ]
