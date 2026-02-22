# chatapp/migrations/0002_create_callrecording.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("chatapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CallRecording",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("caller", models.CharField(max_length=150)),
                ("receiver", models.CharField(max_length=150)),
                ("room_name", models.CharField(blank=True, max_length=150, null=True)),
                ("file_path", models.TextField()),
                ("duration", models.IntegerField(blank=True, null=True)),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("ended_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
