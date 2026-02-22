# Generated manually to rename file_path to file_url in CallRecording

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0005_alter_mediafile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='callrecording',
            old_name='file_path',
            new_name='file_url',
        ),
    ]
