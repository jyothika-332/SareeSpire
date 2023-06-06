from .models import Categories


def menu_link(request):
    links = Categories.objects.all()
    return dict(links=links)