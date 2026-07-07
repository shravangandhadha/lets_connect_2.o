from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect

from .models import Member


def get_current_member(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return None
    try:
        return Member.objects.get(id=member_id)
    except Member.DoesNotExist:
        request.session.flush()
        return None


def _require_login(request):
    return bool(get_current_member(request))


def about(request):
    return render(request, 'about.html', {'member': get_current_member(request)})


def login(request):
    if _require_login(request):
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
        else:
            try:
                member = Member.objects.get(email=email)
            except Member.DoesNotExist:
                member = None
            if member and (check_password(password, member.password) or member.password == password):
                request.session['member_id'] = member.id
                messages.success(request, 'Successfully logged in.')
                return redirect('dashboard')
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    messages.info(request, 'Logged out.')
    return redirect('login')


def register(request):
    if _require_login(request):
        return redirect('dashboard')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        terms = request.POST.get('terms')
        if not name or not email or not password or not confirm_password:
            messages.error(request, 'Please complete all required fields.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif not terms:
            messages.error(request, 'You must agree to the Terms of Service and Privacy Policy.')
        elif Member.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            member = Member.objects.create(
                name=name,
                email=email,
                password=make_password(password),
                gender=request.POST.get('gender', ''),
                age=int(request.POST.get('age', 0) or 0),
                city=request.POST.get('city', ''),
                state=request.POST.get('state', ''),
                country=request.POST.get('country', ''),
                interests=request.POST.get('interests', ''),
            )
            request.session['member_id'] = member.id
            messages.success(request, 'Registration successful.')
            return redirect('dashboard')
    return render(request, 'register.html')


def dashboard(request):
    member = get_current_member(request)
    if not member:
        return redirect('login')
    return render(request, 'dashboard.html', {'member': member})


def profile(request):
    member = get_current_member(request)
    if not member:
        return redirect('login')
    return render(request, 'profile.html', {'member': member})


def edit_profile(request):
    member = get_current_member(request)
    if not member:
        return redirect('login')
    if request.method == 'POST':
        member.name = request.POST.get('name', member.name).strip() or member.name
        member.gender = request.POST.get('gender', member.gender).strip() or member.gender
        member.age = int(request.POST.get('age', member.age) or member.age)
        member.city = request.POST.get('city', member.city).strip() or member.city
        member.state = request.POST.get('state', member.state).strip() or member.state
        member.country = request.POST.get('country', member.country).strip() or member.country
        member.interests = request.POST.get('interests', member.interests).strip() or member.interests
        password = request.POST.get('password', '').strip()
        if password:
            member.password = make_password(password)
        member.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'edit_profile.html', {'member': member})


def browse(request):
    member = get_current_member(request)
    if not member:
        return redirect('login')
    return render(request, 'browse.html', {'member': member})


def view_messages(request):
    member = get_current_member(request)
    if not member:
        return redirect('login')
    return render(request, 'messages.html', {'member': member})


def call(request):
    member = get_current_member(request)
    if not member:
        return redirect('login')
    return render(request, 'call.html', {'member': member})
