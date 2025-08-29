from .forms import ArticleForm
from articles.models import Article
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

def articles_detail_view(request, slug):
    if slug is not None:
        article_obj = get_object_or_404(Article, slug=slug) 
    context = {
        "object":article_obj
    }
    return render(request, "articles/detail.html", context)

@login_required
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
    return render(request, "articles/create.html", context)

@login_required
def articles_update_view(request, id):
    obj = get_object_or_404(Article, id=id)
    print(obj)
    form = ArticleForm(request.POST or None, instance=obj)
    context = {
        "form":form,
        "object":obj
    }
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, "articles/update.html", context) 
