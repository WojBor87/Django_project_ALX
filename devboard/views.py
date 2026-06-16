from django.http import HttpResponse
from django.shortcuts import render

from .models import Comment

# Create your views here.
def index(request):
    name = request.GET.get('name', '1')
    if name != '1':
        comments = Comment.objects.filter()
    else:
        comments = None
    return render(
        request,
        'index.html',
        {'name': name, 'comments': comments}
    )

def http(request):
    return HttpResponse(
        """
        <h1>DevBoard</h1>
            <ul> 
                <li><h2>etap 1: scaffold!</h2></li>
            </ul>
        """
    )
