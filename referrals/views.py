from django.shortcuts import render, redirect
from django.http import Http404
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

def signup(request):
    profile_id = request.session.get('ref_profile')
    form = UserCreationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()

        # Link to referral profile if exists
        if profile_id:
            try:
                recommended_by_profile = Profile.objects.get(id=profile_id)
                user.profile.recommended_by = recommended_by_profile.user
                user.profile.save()
            except Profile.DoesNotExist:
                pass

        # Authenticate the new user
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)

        if user:
            login(request, user)
            return redirect('main-view')

    context = {'form': form}
    return render(request, 'signup.html', context)

def mainview(request, *args, **kwargs):
    code = kwargs.get('referral_code')
    if code:
        try:
            profile = Profile.objects.get(referral_code=code)  # Assuming 'referral_code' is the correct field name
            request.session['ref_profile'] = profile.id
            print(profile.id)
        except Profile.DoesNotExist:
            raise Http404("Profile not found with the provided referral code.")
    else:
        # Handle the case where no referral code is provided
        pass

    # For debugging purposes
    print('Session expiry age:', request.session.get_expiry_age())

    return render(request, 'main.html')

def my_recommendation_view(request):
    profile = Profile.objects.get(user=request.user)
    my_recomendations = profile.get_recommended_profiles()
    context = {'my_recomendations': my_recomendations}
    return render(request, 'recommendation.html', context)
