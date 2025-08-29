from django.shortcuts import render
from articles.models import Article

def home(request):
    query = request.GET.get("q")
    qs = Article.objects.all()
    if query:
        qs = Article.objects.search(query=query)
    context = {
        "objects": qs,
    }
    return render(request, "pages/home.html", context)
