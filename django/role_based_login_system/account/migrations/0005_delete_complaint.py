# Generated by Django 4.2.1 on 2023-05-31 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_category_complaint'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Complaint',
        ),
    ]
