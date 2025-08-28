from articles.models import Article
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm

def articles_detail_view(request, slug):
    if slug is not None:
        article_obj = get_object_or_404(Article, slug=slug) 
    context = {
        "object":article_obj
    }
    return render(request, "pages/articles/detail.html", context)

@login_required(login_url='/accounts/login/')
def articles_create_view(request):
    form = ArticleForm
    context = {
        "form":form
    }
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        context['form'] = form
        if form.is_valid():
            obj = form.save()
            context['form'] = ArticleForm()
            if obj:
                return redirect('home')
    return render(request, "pages/articles/create.html", context)
