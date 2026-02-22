# Generated manually to add attachments_json field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0003_mediafile'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='attachments_json',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
