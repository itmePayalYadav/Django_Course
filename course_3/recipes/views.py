from .models import Recipe
from .forms import RecipeForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        "objects":qs
    }
    return render(request, "recipes/list.html", context)

@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('recipe-list')
    return render(request, "recipes/create.html", context) 

@login_required
def recipe_detail_view(request, slug):
    if slug is not None:
        recipt_obj = get_object_or_404(Recipe, slug=slug, user=request.user) 
    context = {
        "object":recipt_obj
    }
    return render(request, "recipes/detail.html", context) 

@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    context = {
        "form":form,
        "object":obj
    }
    if form.is_valid():
        obj.save()
        return redirect('recipe-list')
    return render(request, "recipes/update.html", context) 

@login_required
def recipe_delete_view(request, id=None):    
    return 
