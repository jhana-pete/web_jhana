# Generated by Django 4.2.1 on 2023-06-02 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_rename_category_complaint_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Complaint',
        ),
    ]
