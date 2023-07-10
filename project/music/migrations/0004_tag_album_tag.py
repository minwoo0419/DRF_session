# Generated by Django 4.2.2 on 2023-07-10 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_alter_track_album'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='tag',
            field=models.ManyToManyField(blank=True, to='music.tag'),
        ),
    ]