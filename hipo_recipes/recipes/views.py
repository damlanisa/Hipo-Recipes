from django.shortcuts import render


posts = [
    {
        'author': 'Damla',
        'title': 'Recipe 1',
        'content': 'First recipe content',
        'date_posted': 'March 10, 2020'
    },
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'recipes/home.html', context)
