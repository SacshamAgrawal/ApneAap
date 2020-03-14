from django.shortcuts import render,redirect
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy

# Create your class-based views here.
# class Sign_Up( CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('homepage')
#     template_name = 'accounts/signup.html'

#     def form_invalid(self, form):
#         print("Error !!! .........",form.errors)
#         return super().form_invalid(form)

# Create your fucntion-based views here.

def homepage(request):
    return render(request,'Booking/homepage.html',{})
