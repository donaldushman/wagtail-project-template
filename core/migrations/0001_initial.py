import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailimages", "0027_image_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="SEOSettings",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("organization_name", models.CharField(blank=True, max_length=255)),
                ("default_social_image", models.ForeignKey(blank=True, help_text="Default image used when a page does not define its own social image.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="wagtailimages.image")),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("logo", models.ForeignKey(blank=True, help_text="Optional site logo displayed in the header.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to="wagtailimages.image")),
                ("site", models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to="wagtailcore.site")),
            ],
            options={"abstract": False},
        ),
    ]
