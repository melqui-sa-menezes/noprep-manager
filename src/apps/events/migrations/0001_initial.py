# Generated by Django 5.1 on 2024-08-29 14:31

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('name', models.CharField(help_text='Nome do tipo de Evento', max_length=30)),
                ('description', models.CharField(blank=True, help_text='Descrição de Evento', max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('name', models.CharField(help_text='Nome do evento', max_length=100)),
                ('date', models.DateField(help_text='Data do Evento')),
                ('star_time', models.TimeField(blank=True, help_text='Horário de Início do Evento', null=True)),
                ('end_time', models.TimeField(blank=True, help_text='Horário de Término do Evento', null=True)),
                ('address', models.CharField(help_text='Endereço do Evento', max_length=256)),
                ('fee', models.DecimalField(blank=True, decimal_places=2, help_text='Taxa de inscrição do Evento', max_digits=7, null=True)),
                ('regulation', models.URLField(blank=True, help_text='Acesso ao link do regulamento do Evento', null=True)),
                ('organizer', models.ForeignKey(help_text='Organizador do Evento', max_length=100, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event_type', models.ForeignKey(help_text='Tipo de Evento', on_delete=django.db.models.deletion.CASCADE, to='events.eventtype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
