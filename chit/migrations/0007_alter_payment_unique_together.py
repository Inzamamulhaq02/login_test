# Generated by Django 5.1.1 on 2024-10-02 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chit', '0006_user_total_pending_amount'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together=set(),
        ),
    ]
