from django.http import response
from django.shortcuts import render
from .forms import adminRegisterForm

# Create your views here.
def registerAdmin(request):
    response = {}
    form = adminRegisterForm(request.POST)
    response['form'] = form
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']





    return render(request,'register.html',response)