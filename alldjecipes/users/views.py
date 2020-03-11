from django.shortcuts import render,HttpResponseRedirect, reverse, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import View
from alldjecipes.users.forms import SignupForm
from alldjecipes.users.models import ChefUser
from alldjecipes.recipes.models import Recipe

class AddUser(View):
    html = 'generic_form.html'
    def get(self, request):
        form = SignupForm()
        return render(request, self.html, {'form': form})
    def post(self, request):
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_recipe = ChefUser.objects.create_user(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    username=data['username'],
                    password=data['password'],
                )
            return HttpResponseRedirect(reverse('login'))
        form = SignupForm()
        return render(request, html, {'form': form})


def user_view(request, id):
    html = 'chefuser.html'
    chefuser = ChefUser.objects.filter(id=id).first()
    recipes = Recipe.objects.filter(creator=chefuser)
    return render(request, html, {'chefuser':chefuser, 'recipes':recipes})

def all_users_view(request):
    html = 'allusers.html'
    chefuser = ChefUser.objects.all().order_by('date_joined')
    return render(request, html, {'chefusers':chefuser})

def number_of_users(request):
    allusers = ChefUser.objects.all()
    numberusers = ChefUser.objects.count()
    return render(request, 'AllDjecipes/alldjecipes/templates/index.html', {'users': allusers, 'usercount': numberusers})
    