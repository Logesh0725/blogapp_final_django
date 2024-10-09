from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, BlogForm
from .models import Blog,Comment
from .forms import CommentForm


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('header')
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'blog/login.html')

@login_required
def dashboard(request):
    blogs = Blog.objects.filter(author=request.user)
    return render(request, 'blog/dashboard.html', {'blogs': blogs})

@login_required
def create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('dashboard')
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})

@login_required
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/blog_list.html', {'blogs': blogs})

@login_required
@login_required
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    is_liked = blog.likes.filter(id=request.user.id).exists()
    is_disliked = blog.dislikes.filter(id=request.user.id).exists()  # Check if user disliked

    # Initialize forms
    comment_form = CommentForm()  # Initialize comment form

    if request.method == "POST":
        # Check for comment submission
        if 'comment' in request.POST:
            comment_form = CommentForm(request.POST)  # Create a comment form instance with submitted data
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.blog = blog
                new_comment.author = request.user
                new_comment.save()
                return redirect('blog_detail', blog_id=blog.id)

    

   
        # Check for like submission
    elif 'like' in request.POST:
            if is_liked:
                blog.likes.remove(request.user)
            else:
                blog.likes.add(request.user)
            return redirect('blog_detail', blog_id=blog.id)

        # Check for dislike submission
    elif 'dislike' in request.POST:
            if is_disliked:
                blog.dislikes.remove(request.user)
            else:
                blog.dislikes.add(request.user)
            return redirect('blog_detail', blog_id=blog.id)

    comments = blog.comments.all()  # Retrieve all comments for the blog

    # Render the template with all required data
    return render(request, 'blog/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form,  # Pass the comment form
        'is_liked': is_liked,
        'is_disliked': is_disliked,     # Pass dislike status
        'total_likes': blog.total_likes(),
        'total_dislikes': blog.total_dislikes(),  # Pass total dislikes

    })



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def header(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/header.html', {'blogs': blogs})

def contact(request):
    return render(request, 'blog/contact.html')

@login_required
def profile(request):
    user_blogs = Blog.objects.filter(author=request.user)

    # Handle the blog update
    if request.method == "POST" and 'update_blog' in request.POST:
        blog_id = request.POST.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id, author=request.user)

        # Update the blog title and content
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title:
            blog.title = title
        if content:
            blog.content = content
        
        # Handle the uploaded image
        if request.FILES.get('image'):
            uploaded_file = request.FILES['image']
            fs = FileSystemStorage()
            if blog.image_url:  # Check if there's an old image
                fs.delete(blog.image_url.name)  # Delete old image file
            filename = fs.save(uploaded_file.name, uploaded_file)
            blog.image_url = fs.url(filename)  # Update image URL

        blog.save() 
        return redirect('profile')

    
    if request.method == "POST" and 'delete_blog' in request.POST:
        blog_id = request.POST.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id, author=request.user)
        blog.delete()
        return redirect('profile')

    return render(request, 'blog/profile.html', {'blogs': user_blogs})


@login_required
def mine(request):
    user_blogs = Blog.objects.filter(author=request.user)
    
    return render(request, 'blog/mine.html', {'blogs': user_blogs})
