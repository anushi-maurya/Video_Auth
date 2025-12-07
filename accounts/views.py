from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

def register(request):
    # If the form was submitted
    if request.method == "POST":
        # Fill the form with user input
        form = RegisterForm(request.POST)

        # Check if form data is valid
        if form.is_valid():
            # Create a new user in the database
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            # Show success message
            messages.success(
                request,
                f"New user {form.cleaned_data['username']} is registered successfully!"
            )

            # Redirect user to home page
            return redirect('videos:home')

    else:
        # If request is GET, show an empty form
        form = RegisterForm()

    # Render the register page and send the form to the template
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('accounts:login')

