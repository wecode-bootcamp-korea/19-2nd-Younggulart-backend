# Generated by Django 3.2 on 2021-04-27 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('arts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('location', models.CharField(max_length=100)),
                ('latitude_x', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('longitude_y', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
            ],
            options={
                'db_table': 'auctions',
            },
        ),
        migrations.CreateModel(
            name='AuctionUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bids.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'auction_users',
            },
        ),
        migrations.CreateModel(
            name='AuctionArt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arts.art')),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bids.auction')),
            ],
            options={
                'db_table': 'auction_arts',
            },
        ),
        migrations.AddField(
            model_name='auction',
            name='art',
            field=models.ManyToManyField(through='bids.AuctionArt', to='arts.Art'),
        ),
        migrations.AddField(
            model_name='auction',
            name='subscriber',
            field=models.ManyToManyField(through='bids.AuctionUser', to='users.User'),
        ),
    ]
