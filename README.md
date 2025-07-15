
⸻

🏗️ 1. Project and App Setup

<details>
<summary>Expand if you need setup commands (otherwise skip to code)</summary>


python -m venv venv
source venv/bin/activate
pip install django requests
django-admin startproject extapi_demo
cd extapi_demo
python manage.py startapp posts

Add 'posts' to INSTALLED_APPS in extapi_demo/settings.py.

</details>



⸻

📁 2. Directory & Files

Create this structure (see only files you need to edit/create):

extapi_demo/
│
├── extapi_demo/
│    └── urls.py
├── posts/
│    ├── urls.py
│    ├── views.py
│    └── templates/
│         └── posts/
│              ├── post_list.html
│              ├── post_detail.html
│              ├── post_form.html
│              └── post_confirm_delete.html


⸻

🌐 3. URL Configuration

Project URLs (extapi_demo/urls.py)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('posts/', include('posts.urls')),
]

App URLs (posts/urls.py)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.post_update, name='post_update'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
]


⸻

🧠 4. Views (Controller Layer)

Paste this in posts/views.py:

import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404

API_BASE = 'https://jsonplaceholder.typicode.com/posts'

def post_list(request):
    try:
        res = requests.get(API_BASE, timeout=5)
        posts = res.json()
    except Exception:
        posts = []
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, pk):
    try:
        res = requests.get(f'{API_BASE}/{pk}', timeout=5)
        if res.status_code == 404:
            raise Http404
        post = res.json()
    except Exception:
        raise Http404
    return render(request, 'posts/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'body': request.POST.get('body'),
            'userId': 1  # dummy user
        }
        res = requests.post(API_BASE, json=data)
        # JSONPlaceholder fakes creation; it returns id=101 always.
        if res.status_code in (200, 201):
            return redirect('post_list')
    return render(request, 'posts/post_form.html', {'action': 'Create'})

def post_update(request, pk):
    # Fetch existing post for form
    try:
        get_res = requests.get(f'{API_BASE}/{pk}', timeout=5)
        if get_res.status_code == 404:
            raise Http404
        post = get_res.json()
    except Exception:
        raise Http404

    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'body': request.POST.get('body'),
            'userId': post.get('userId', 1)
        }
        res = requests.put(f'{API_BASE}/{pk}', json=data)
        if res.status_code in (200, 201):
            return redirect('post_detail', pk=pk)
    return render(request, 'posts/post_form.html', {'post': post, 'action': 'Update'})

def post_delete(request, pk):
    if request.method == 'POST':
        res = requests.delete(f'{API_BASE}/{pk}')
        if res.status_code in (200, 204):
            return redirect('post_list')
    try:
        res = requests.get(f'{API_BASE}/{pk}')
        if res.status_code == 404:
            raise Http404
        post = res.json()
    except Exception:
        raise Http404
    return render(request, 'posts/post_confirm_delete.html', {'post': post})


⸻

🖼️ 5. Templates

a) post_list.html

<!DOCTYPE html>
<html>
<head><title>All Posts</title></head>
<body>
    <h1>All Posts</h1>
    <a href="{% url 'post_create' %}">Create New Post</a>
    <ul>
    {% for post in posts %}
        <li>
            <a href="{% url 'post_detail' post.id %}">{{ post.title }}</a>
            [<a href="{% url 'post_update' post.id %}">Edit</a>]
            [<a href="{% url 'post_delete' post.id %}">Delete</a>]
        </li>
    {% empty %}
        <li>No posts found.</li>
    {% endfor %}
    </ul>
</body>
</html>

b) post_detail.html

<!DOCTYPE html>
<html>
<head><title>{{ post.title }}</title></head>
<body>
    <h2>{{ post.title }}</h2>
    <p>{{ post.body }}</p>
    <a href="{% url 'post_update' post.id %}">Edit</a>
    <a href="{% url 'post_delete' post.id %}">Delete</a>
    <br><a href="{% url 'post_list' %}">Back to List</a>
</body>
</html>

c) post_form.html

<!DOCTYPE html>
<html>
<head><title>{{ action }} Post</title></head>
<body>
    <h2>{{ action }} Post</h2>
    <form method="post">
        {% csrf_token %}
        <label>Title:<br>
            <input type="text" name="title" value="{{ post.title|default_if_none:'' }}">
        </label><br><br>
        <label>Body:<br>
            <textarea name="body" rows="4" cols="40">{{ post.body|default_if_none:'' }}</textarea>
        </label><br><br>
        <button type="submit">{{ action }}</button>
    </form>
    <a href="{% url 'post_list' %}">Back to List</a>
</body>
</html>

d) post_confirm_delete.html

<!DOCTYPE html>
<html>
<head><title>Delete Post</title></head>
<body>
    <h2>Delete Post: {{ post.title }}</h2>
    <p>Are you sure you want to delete this post?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Yes, Delete</button>
        <a href="{% url 'post_detail' post.id %}">Cancel</a>
    </form>
</body>
</html>


⸻

🚀 6. Run the App

python manage.py migrate
python manage.py runserver

Go to http://localhost:8000/posts/

⸻
