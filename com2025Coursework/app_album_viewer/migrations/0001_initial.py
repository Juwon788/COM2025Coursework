# Generated by Django 4.2.5 on 2023-12-07 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(blank=True, default='default_cover/default.png', null=True, upload_to='default_cover/')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('artist', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('format', models.CharField(max_length=50)),
                ('release_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('firstname', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('runtime', models.IntegerField()),
                ('albums', models.ManyToManyField(related_name='songs', to='app_album_viewer.album')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=100)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app_album_viewer.album')),
            ],
        ),
    ]
