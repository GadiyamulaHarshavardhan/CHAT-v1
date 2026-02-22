from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0004_add_attachments_json_to_message'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MediaFile',
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_url', models.TextField()),
                ('media_type', models.CharField(max_length=20)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('duration', models.CharField(blank=True, max_length=20)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_files', to='chatapp.message')),
            ],
        ),
    ]
