from django import forms
from alldjecipes.recipes.models import Recipe, Comment

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'recipe_name',
            'difficulty',
            'vegitarian',
            'vegan',
            'category',
            'ingredients',
            'instructions',
            'completion_time',
            'image'
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]