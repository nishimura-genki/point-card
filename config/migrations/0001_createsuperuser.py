from django.db import migrations

import google.auth
from google.cloud import secretmanager_v1 as sm


def createsuperuser(apps, schema_editor):
    _, project = google.auth.default()
    client = sm.SecretManagerServiceClient()
    name = f"projects/{project}/secrets/admin_password/versions/latest"
    admin_password = client.access_secret_version(
        name=name).payload.data.decode("UTF-8")

    from django.contrib.auth import get_user_model
    User = get_user_model()
    User.objects.create_superuser('admin@admin.com', password=admin_password)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunPython(createsuperuser)
    ]
