from django.shortcuts import render

from basepage.models import BasePage


def search(request):
    search_query = request.GET.get("query", "").strip()
    search_results = BasePage.objects.none()

    if search_query:
        search_results = BasePage.objects.live().public().search(search_query)

    return render(
        request,
        "core/search.html",
        {"search_query": search_query, "search_results": search_results},
    )
