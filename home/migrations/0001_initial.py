from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("basepage", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePage",
            fields=[
                (
                    "basepage_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="basepage.basepage",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("basepage.basepage",),
        ),
    ]
