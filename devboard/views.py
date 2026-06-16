from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    name = request.GET.get('name', 'Guest')
    number = request.GET.get('number', 1)
    return render(request, 'index.html', {'name': name, 'number': number})

def http(request):
    return HttpResponse(
        """
        <h1>DevBoard</h1>
            <ul> 
                <li><h2>etap 1: scaffold!</h2></li>
            </ul>
        """
    )
