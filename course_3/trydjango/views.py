from django.shortcuts import render
from django.db.models import Q
from articles.models import Article

def home(request):
    query = request.GET.get("q")
    objects = Article.objects.all()
    if query:
        objects = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    context = {
        "query": query,
        "objects": objects,
    }
    return render(request, "pages/home.html", context)
