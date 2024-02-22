# Generated by Django 4.2.10 on 2024-02-22 07:06

import apps.blog.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields
import utils.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(blank=True, default=False)),
                ('name', models.CharField(max_length=127, unique=True)),
                ('thumbnail', models.ImageField(default='default/default.png', upload_to=utils.utils.category_path)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(blank=True, default=False)),
                ('body', django_ckeditor_5.fields.CKEditor5Field()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(blank=True, default=False)),
                ('body', django_ckeditor_5.fields.CKEditor5Field()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_replies', to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.comment')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(blank=True, default=False)),
                ('title', models.CharField(max_length=255)),
                ('preview_body', models.TextField(default='Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus laborum autem, dolores inventore, beatae nam.', max_length=127)),
                ('body', django_ckeditor_5.fields.CKEditor5Field()),
                ('thumbnail', models.ImageField(default='default/default.png', upload_to=apps.blog.utils.post_path)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(blank=True, default=False)),
                ('format', models.CharField(choices=[('JPEG', 'jpeg'), ('JPG', 'jpg'), ('PNG', 'png'), ('GIF', 'gif'), ('BMP', 'bmp'), ('SVG', 'svg'), ('WebP', 'webp'), ('TIFF', 'tiff'), ('MP4', 'mp4'), ('AVI', 'avi'), ('MKV', 'mkv'), ('MOV', 'mov'), ('WMV', 'wmv'), ('FLV', 'flv'), ('WebM', 'webm'), ('MP3', 'mp3'), ('WAV', 'wav'), ('AAC', 'aac'), ('FLAC', 'flac'), ('OGG', 'ogg'), ('M4A', 'm4a'), ('AIFF', 'aiff')], editable=False, max_length=5)),
                ('type', models.CharField(choices=[('IMAGE', 'Image'), ('VIDEO', 'Video'), ('AUDIO', 'Audio')], editable=False, max_length=5)),
                ('file', models.FileField(upload_to=apps.blog.utils.gallery_path)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_files', to='blog.post')),
            ],
            options={
                'verbose_name': 'gallery',
                'verbose_name_plural': 'galleries',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='blog.post'),
        ),
        migrations.CreateModel(
            name='CategoryPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(blank=True, default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='blog.category')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='blog.post')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(blank=True, default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to='blog.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'post')},
            },
        ),
    ]