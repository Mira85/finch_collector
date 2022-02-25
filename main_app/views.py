from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch
from .models import Toy
# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def finches_index(request):
    finches = Finch.objects.all()
    print('finches',finches)
    return render(request, 'finches/index.html', {'finches': finches})

def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    return render(request, 'finches/detail.html', {'finch': finch})


class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'

class FinchUpdate(UpdateView):
    model = Finch
    fields = ('description', 'habitat', 'lifespan', 'sound')

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches/'
    
class ToysList(ListView):
    model = Toy
    template_name = 'toys/index.html'
    context_object_name = 'toys'
    queryset = Toy.objects.all()

class ToyDetail(DetailView):
    model = Toy
    template_name ='toys/detail.html'

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ( 'name', 'color')

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

