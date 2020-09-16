# Generated by Django 3.0.10 on 2020-09-16 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20200807_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='formfield',
            name='clean_name',
            field=models.CharField(blank=True, default='', help_text='Safe name of the form field, the label converted to ascii_snake_case', max_length=255, verbose_name='name'),
        ),
    ]
