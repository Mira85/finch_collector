from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Finch, Toy, Photo
from .forms import FeedingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


import boto3
import uuid

S3_BASE_URL ='https://s3.us-east-1.amazonaws.com/'
BUCKET = 'finch-collector1'
session = boto3.Session(profile_name='finch-collector1')


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def finches_index(request):
    finches = Finch.objects.filter(user = request.user)
    print('finches',finches)
    return render(request, 'finches/index.html', {'finches': finches})


@login_required
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    feeding_form = FeedingForm()

    toys_finch_doesnt_have = Toy.objects.exclude(id__in =finch.toys.all().values_list('id'))

    return render(request, 'finches/detail.html', {
        'finch': finch, 
        'feeding_form': feeding_form,
        'toys': toys_finch_doesnt_have
        })


@login_required
def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    print(form.errors)
    if form.is_valid():
        print('valid')
        new_feeding = form.save(commit = False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id = finch_id)


@login_required
def assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.add(toy_id)
    return redirect('detail', finch_id=finch_id)


@login_required
def add_photo(request, finch_id):
    photo_file = request.FILES.get('photo-file')
    if photo_file:
        s3 = session.client('s3')
        key = uuid.uuid4().hex[:6]+ photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            photo = Photo(url=url, finch_id=finch_id)

            photo.save()

        except Exception as error:
            print('**************************')
            print('An error occurred while upoading to S3')
            print(error)
            print('**************************')

    return redirect('detail', finch_id=finch_id)


@login_required
def remove_assoc_toy(request, finch_id, toy_id):
    Finch.objects.get(id=finch_id).toys.remove(toy_id)
    return redirect('detail', finch_id=finch_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'invalid sign up - please try again'



    form = UserCreationForm()
    context = {'form': form, 'error': error_message }
    return render(request, 'registration/signup.html', context)
           
    

class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ('description', 'habitat', 'lifespan', 'sound')

class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = '/finches/'
    
class ToysList(LoginRequiredMixin, ListView):
    model = Toy
    template_name = 'toys/index.html'
    context_object_name = 'toys'
    queryset = Toy.objects.all()

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    template_name ='toys/detail.html'

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ( 'name', 'color')

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

