from django import template

register = template.Library()


@register.simple_tag
def get_menu_pages():
    from basepage.models import BasePage

    return BasePage.objects.live().public().in_menu().filter(depth=3)


@register.simple_tag
def get_submenu_pages(parent):
    return parent.get_children().live().public().in_menu().specific()


@register.simple_tag(takes_context=True)
def menu_page_state(context, menu_page):
    current_page = context.get("page")
    if not current_page:
        return ""
    if current_page.pk == menu_page.pk:
        return "current"
    if current_page.is_descendant_of(menu_page):
        return "ancestor"
    return ""
