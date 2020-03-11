from django.shortcuts import render,HttpResponseRedirect, reverse, HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from alldjecipes.recipes.forms import CommentForm, RecipeForm
from alldjecipes.recipes.models import Recipe, Comment, Vote
from alldjecipes.recipes.models import ChefUser
from alldjecipes.helpers.helper import voting_helper


def index(request):
    html = "index.html"
    recipe = Recipe.objects.all()
    numberrecipes = Recipe.objects.count()
    return render(request, html, {"recipe": recipe, 'recipecount': numberrecipes})


def recipe_detail(request, id):
    html = 'recipeview.html'
    user = ChefUser.objects.filter(id=id)
    logged = request.user
    recipe = Recipe.objects.filter(id=id).first()
    comments = Comment.objects.filter(recipebase=recipe).order_by("-date")
    ingredients, instructions = recipe.ingredients, recipe.instructions
    if '.' in ingredients or instructions:
        ingredients, instructions = recipe.ingredients.split('.'), recipe.instructions.split('.')

    return render(request, html, {"ingredients": ingredients, "instructions": instructions, "recipe": recipe, 'comments':comments, 'user': user, 'logged':logged})


@method_decorator(login_required, name='dispatch')
class AddRecipe(View):
    html = 'generic_form.html'
    def get(self, request):
        form = RecipeForm()
        return render(request, self.html, {'form': form})
    def post(self, request):
        if request.method == 'POST':
            form = RecipeForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                new_recipe = Recipe.objects.create(
                    creator=request.user,
                    recipe_name=data['recipe_name'],
                    difficulty=data['difficulty'],
                    vegitarian=data['vegitarian'],
                    vegan=data['vegan'],
                    category=data['category'],
                    ingredients=data['ingredients'],
                    instructions=data['instructions'],
                    completion_time=data['completion_time'],
                    image=data['image'],
                    contact=request.user.email
                    )
            return HttpResponseRedirect(reverse('chefuser',  args=[request.user.id]))
        form = RecipeForm()
        return render(request, html, {'form': form})

@method_decorator(login_required, name='dispatch')
class AddComment(View):
    html = 'generic_form.html'
    def get(self, request,id):
        form = CommentForm()
        return render(request, self.html, {'form': form})
    def post(self, request, id):
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_recipe = Comment.objects.create(
                    recipebase=Recipe.objects.filter(id=id).first(),
                    commentor=request.user,
                    content=data['content'],
                    )
            return HttpResponseRedirect(reverse('recipe_detail', args=[id]))
        form = CommentForm()
        return render(request, html, {'form': form})


def filter_by_category(request, param):
    html = 'category_filter.html'
    category_items =  Recipe.objects.filter(category=param.lower().title()).order_by('-date')
    return render(request, html, {'category_item': category_items})


@login_required
def recipe_upvote(request, id):
    html = "recipeview.html"
    voting_helper(id, Recipe, 'upvote')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@login_required
def comment_upvote(request, id):
    html = "recipeview.html"
    voting_helper(id, Comment, 'upvote')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


@login_required
def recipe_downvote(request, id):
    html = "recipeview.html"
    voting_helper(id, Recipe, 'downvote')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@login_required
def comment_downvote(request, id):
    html = "recipeview.html"
    voting_helper(id, Comment, 'downvote')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

def edit_recipe_view(request,id):
    html = "generic_form.html"
    instance = Recipe.objects.get(id=id)
    logged_in = request.user
    if logged_in == instance.creator:
        if request.method == "POST":
            form = RecipeForm(request.POST, instance=instance)
            form.save()
            return HttpResponseRedirect(reverse('recipe_detail', args=[id]))
    else:
        return HttpResponse("You can't do that")
    form = RecipeForm(instance=instance)
    return render(request, html, {'form': form})

def number_of_recipes(request):
    allrecipes = Recipe.objects.all()
    numberrecipes = Recipe.objects.count()
    return render(request, './templates/index.html', {'recipes': allrecipes, 'recipecount': numberrecipes})
