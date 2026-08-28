from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from datetime import datetime

from .models import Member
from .models import Post
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def get_current_member(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return None

    member = Member.objects.filter(id=member_id).first()
    if not member:
        request.session.flush()
    return member


def _parse_age(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _parse_date(value):
    if not value:
        return None
    try:
        # Expect YYYY-MM-DD or ISO formats
        return datetime.fromisoformat(value).date()
    except Exception:
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except Exception:
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
            member = Member.objects.filter(email__iexact=email).first()
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
        elif Member.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            member = Member.objects.create(
                name=name,
                display_name=request.POST.get('display_name', '').strip(),
                email=email,
                password=make_password(password),
                avatar_url=request.POST.get('avatar_url', '').strip(),
                bio=request.POST.get('bio', '').strip(),
                phone=request.POST.get('phone', '').strip(),
                dob=_parse_date(request.POST.get('dob', '').strip()),
                website=request.POST.get('website', '').strip(),
                github=request.POST.get('github', '').strip(),
                linkedin=request.POST.get('linkedin', '').strip(),
                gender=request.POST.get('gender', ''),
                age=_parse_age(request.POST.get('age', 0), 0),
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
        member.display_name = request.POST.get('display_name', member.display_name).strip() or member.display_name
        member.avatar_url = request.POST.get('avatar_url', member.avatar_url).strip() or member.avatar_url
        member.bio = request.POST.get('bio', member.bio).strip() or member.bio
        member.phone = request.POST.get('phone', member.phone).strip() or member.phone
        dob_val = _parse_date(request.POST.get('dob', ''))
        if dob_val is not None:
            member.dob = dob_val
        member.website = request.POST.get('website', member.website).strip() or member.website
        member.github = request.POST.get('github', member.github).strip() or member.github
        member.linkedin = request.POST.get('linkedin', member.linkedin).strip() or member.linkedin
        member.gender = request.POST.get('gender', member.gender).strip() or member.gender
        member.age = _parse_age(request.POST.get('age', member.age), member.age)
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


def posts_list(request):
    member = get_current_member(request)
    if not member:
        return redirect('login')
    posts = Post.objects.filter(is_published=True).select_related('author')[:50]
    return render(request, 'posts.html', {'member': member, 'posts': posts})


def create_post(request):
    member = get_current_member(request)
    if not member:
        return redirect('login')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if not title or not content:
            messages.error(request, 'Please provide both a title and content.')
        else:
            Post.objects.create(author=member, title=title, content=content)
            messages.success(request, 'Post created.')
            return redirect('posts')
    return render(request, 'create_post.html', {'member': member})


def post_detail(request, post_id):
    member = get_current_member(request)
    if not member:
        return redirect('login')
    post = Post.objects.filter(id=post_id, is_published=True).select_related('author').first()
    if not post:
        messages.error(request, 'Post not found.')
        return redirect('posts')
    return render(request, 'post_detail.html', {'member': member, 'post': post})


@require_http_methods(['GET'])
def api_profile(request, member_id):
    m = Member.objects.filter(id=member_id).first()
    if not m:
        return JsonResponse({'error': 'not found'}, status=404)
    data = {
        'id': m.id,
        'name': m.name,
        'display_name': m.display_name,
        'email': m.email,
        'bio': m.bio,
        'avatar_url': m.avatar_url,
        'city': m.city,
        'state': m.state,
        'country': m.country,
        'interests': m.interests,
    }
    return JsonResponse(data)


@require_http_methods(['GET'])
def api_posts(request):
    qs = Post.objects.filter(is_published=True).select_related('author')[:100]
    data = []
    for p in qs:
        data.append({'id': p.id, 'title': p.title, 'content': p.content, 'author': p.author.id, 'author_name': str(p.author), 'created_at': p.created_at.isoformat()})
    return JsonResponse({'posts': data})


@require_http_methods(['GET'])
def api_post_detail(request, post_id):
    p = Post.objects.filter(id=post_id, is_published=True).select_related('author').first()
    if not p:
        return JsonResponse({'error': 'not found'}, status=404)
    data = {'id': p.id, 'title': p.title, 'content': p.content, 'author': p.author.id, 'author_name': str(p.author), 'created_at': p.created_at.isoformat()}
    return JsonResponse(data)
