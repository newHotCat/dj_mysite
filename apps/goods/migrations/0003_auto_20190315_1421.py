# Generated by Django 2.1.7 on 2019-03-15 14:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20190315_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, verbose_name='品牌名称')),
                ('desc', models.TextField(default='', max_length=200, verbose_name='品牌描述')),
                ('image', models.CharField(max_length=200, verbose_name='品牌LOGO')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
        ),
        migrations.AlterModelOptions(
            name='good',
            options={'verbose_name': '商品', 'verbose_name_plural': '商品'},
        ),
        migrations.AddField(
            model_name='good',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AddField(
            model_name='good',
            name='brands',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='goods.GoodBrand', verbose_name='品牌'),
        ),
    ]
