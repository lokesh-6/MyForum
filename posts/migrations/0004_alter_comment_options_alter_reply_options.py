# Generated by Django 4.2.6 on 2023-10-16 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_reply_comment_post_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={},
        ),
        migrations.AlterModelOptions(
            name='reply',
            options={'verbose_name_plural': 'replies'},
        ),
    ]