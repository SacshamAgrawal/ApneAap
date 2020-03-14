# Generated by Django 3.0.4 on 2020-03-12 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('boarding_station_code', models.CharField(max_length=4)),
                ('destination_station_code', models.CharField(max_length=4)),
                ('no_of_tickets', models.IntegerField(default=1, verbose_name='No. of Tickets')),
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
        ),
    ]
