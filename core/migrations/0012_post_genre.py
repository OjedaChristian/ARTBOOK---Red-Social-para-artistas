# Generated by Django 4.1.5 on 2023-01-31 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_delete_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='genre',
            field=models.CharField(choices=[('Fantasy', 'Fantasy'), ('Ilustración', 'Ilustración'), ('Conceptual', 'Conceptual'), ('Paisajes', 'Paisajes'), ('Diseño', 'Diseño'), ('Retratos', 'Retratos')], default='General', max_length=11),
        ),
    ]
