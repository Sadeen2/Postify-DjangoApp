from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post

# Signup (create account)
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            return redirect("login")
        else:
            return render(request, "signup.html", {"error": "Username already exists"})
    return render(request, "signup.html")

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("post_list")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    return render(request, "login.html")

# Logout
def logout_view(request):
    logout(request)
    return redirect("login")

# Show all posts (protected page)
@login_required
def post_list(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, "post_list.html", {"posts": posts})

# Create a new post (protected)
@login_required
def post_create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        Post.objects.create(author=request.user, title=title, content=content)
        return redirect("post_list")
    return render(request, "post_create.html")

@login_required
def post_delete(request, id):
    post = Post.objects.get(id=id, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("post_list")
    return render(request, "post_delete.html", {"post": post})

