# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 18:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('authority', models.CharField(blank=True, max_length=32)),
                ('licnumber', models.CharField(blank=True, max_length=32)),
                ('url', models.CharField(blank=True, max_length=128)),
                ('expdate', models.CharField(blank=True, max_length=16, null=True)),
                ('neverexp', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degreetype', models.CharField(blank=True, max_length=32)),
                ('major', models.CharField(blank=True, max_length=32)),
                ('university', models.CharField(max_length=32)),
                ('date', models.CharField(blank=True, max_length=16, null=True)),
                ('gpa', models.CharField(blank=True, max_length=8)),
                ('honors', models.CharField(blank=True, max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=32)),
                ('startdate', models.CharField(blank=True, max_length=16, null=True)),
                ('enddate', models.CharField(blank=True, max_length=16, null=True)),
                ('jobfunctions', models.TextField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objective', models.TextField(blank=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=32)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.Resume')),
            ],
        ),
        migrations.AddField(
            model_name='employment',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.Resume'),
        ),
        migrations.AddField(
            model_name='degree',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.Resume'),
        ),
        migrations.AddField(
            model_name='certification',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.Resume'),
        ),
    ]
