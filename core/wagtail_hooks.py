from django.conf import settings
from django.urls import reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem


@hooks.register("register_admin_menu_item")
def register_visit_site_menu_item():
    return MenuItem(
        "Visit site",
        settings.BASE_URL,
        icon_name="site",
        order=1,
    )


@hooks.register("construct_help_menu")
def add_technical_guide_menu_item(request, menu_items):
    menu_items.append(
        MenuItem(
            f"{settings.WAGTAIL_SITE_NAME} Technical Guide",
            reverse("protected_docs:index"),
            icon_name="help",
            order=100,
        )
    )
