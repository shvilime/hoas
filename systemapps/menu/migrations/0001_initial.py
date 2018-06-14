# Generated by Django 2.0.5 on 2018-06-14 14:31

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('url', models.CharField(help_text='Ссылка /faq/ или http://google.com', max_length=100, verbose_name='Cсылка')),
                ('active', models.BooleanField(default=True, help_text='Включить/Выключить пункт меню', verbose_name='Активность')),
                ('login_required', models.BooleanField(default=False, help_text='Показывать пункт меню только для авторизованных пользователей', verbose_name='Авторизация')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menuitems', to='menu.Menu', verbose_name='Меню')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='menu.MenuItem', verbose_name='Родительское меню')),
            ],
            options={
                'verbose_name': 'Пункт меню',
                'verbose_name_plural': 'Пункты меню',
            },
        ),
    ]
