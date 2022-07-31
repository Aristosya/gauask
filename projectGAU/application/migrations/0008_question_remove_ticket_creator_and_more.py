# Generated by Django 4.0.2 on 2022-07-30 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0007_alter_ticket_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('question', models.TextField(verbose_name='Question')),
                ('answer', models.TextField(blank=True, default=None, null=True)),
                ('status', models.TextField(blank=True, default='Not read yet', null=True)),
                ('isDone', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ('-id',),
            },
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='lecturer',
        ),
        migrations.DeleteModel(
            name='Lecturer',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
