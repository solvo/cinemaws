# Generated by Django 2.2.7 on 2019-11-20 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvtheater', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='qrcode',
            field=models.FileField(blank=True, null=True, upload_to='qrcode/', verbose_name='QR code'),
        ),
    ]
