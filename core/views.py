from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Follow, Like
# Create your views here.

def getHeader(event):
    if event == 'all':
        return {'name': 'All', 'intro': 'Yeshwantrao Chavan College of Engineering (YCCE), Nagpur, India, organizes anual event as well as various departmental events throughout the year. These events provide an opportunity for the students to showcase their talents and skills and also provide a platform for networking.'}
    elif event == 'compufest':
        return {'name': 'CompuFest', 'intro': 'The event organized by the Department of Computer Technology. Compufest is one of the biggest events in the college and has been held for more than a decade. It is divided into three sections - programming, gaming, and robotics. It also includes an array of fun activities like Quizzes, LAN Gaming, and Hackathons. The events are conducted by students itself in guidance of faculties.'}
    elif event == 'upsurge':
        return {'name': 'UpSurge', 'intro': 'The event organized by the Department of Computer Science Engineering has been a platform for students to show off their skills in programming and gaming. It also provides a great opportunity for them to network with professionals from the industry and interact with fellow peers. The event also promotes innovation and encourages students to think out of the box.'}
    elif event == 'yash':
        return {'name': 'YASH', 'intro': 'YCCE (Yashwantrao Chavan College of Engineering) is one of the leading engineering colleges in India. The college organizes a number of interesting events throughout the year. One of the most popular annual events at YCCE - YASH.'}
    elif event == 'itechroots':
        return {'name': 'iTechRoots', 'intro': 'The event organized by the Department of Information Technology. Event provide an excellent platform for students to explore their interests, develop their skills, and make valuable connections with experts in their fields.'}
    elif event == 'icon':
        return {'name': 'ICON', 'intro': 'The event organized by the Department of Electronics Engineering and Department of Electronics and Telecommunication. Event provide an excellent platform for students to explore their interests, develop their skills, and make valuable connections with experts in their fields.'}
    elif event == 'electrica':
        return {'name': 'Electrica', 'intro': 'The event organized by the Department of Electrical Engineering. Event provide an excellent platform for students to explore their interests, develop their skills, and make valuable connections with experts in their fields.'}
    elif event == 'antaheen':
        return {'name': 'ANTAHEEN', 'intro': 'The event organized by the Department of Civil Engineering. Event provide an excellent platform for students to explore their interests, develop their skills, and make valuable connections with experts in their fields.'}
    elif event == 'mechfiesta':
        return {'name': 'MechFiesta', 'intro': 'The event organized by the Department of Mechanical Engineering. Event provide an excellent platform for students to explore their interests, develop their skills, and make valuable connections with experts in their fields.'}  
    elif event == 'sparsh':
        return {'name': 'Sparsh', 'intro': 'Event provide an excellent platform for students to explore their interests, develop their skills, and make valuable connections with experts in their fields.'}
    elif event == 'other':
        return {'name': 'Personal Posts', 'intro': 'These are personal posts on site. Look around. Explore.'}
    return {}
        
@login_required(login_url='login')
def home(request):
    post_base = Post.objects.all()
    posts = []
    for post in post_base:
        if Follow.objects.filter(follower=request.user.username, following=post.user).exists():
            user_model = User.objects.get(username=post.user)
            profile = Profile.objects.get(user=user_model)
            posts.append({'post':post, 'profile': profile})
    posts = posts[::-1]
    return render(request, 'index.html', {'posts': posts})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else :
            messages.info(request, "User not found!")
            return redirect('login')
    return render(request, 'auth/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        name = request.POST.get('name')

        error = False
        if ' ' in username:
            messages.info(request, "Username must not contain space!")
            error = True
        if len(username) < 4:
            messages.info(request, "Username length is too short!")
            error = True
        if User.objects.all().filter(username=username).exists():
            messages.info(request, "Username is already taken!")
            error = True
        if User.objects.all().filter(email=email).exists():
            messages.info(request, "Email is already taken!")
            error = True
        if error:
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password, email=email, first_name=name)
        user.save()
        #create user_model
        user = User.objects.all().get(username=username)
        model_user = Profile.objects.create(user=user, userid=user.id)
        model_user.save()
        return redirect('login')
    return render(request, 'auth/signup.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def events(request, pk):
    post_base = None
    if pk == 'all':
        post_base = Post.objects.all()
    else:
        post_base = Post.objects.filter(post_event=pk)
    posts = []
    for post in post_base:
        user_model = User.objects.get(username=post.user)
        profile = Profile.objects.get(user=user_model)
        posts.append({'post':post, 'profile': profile})
    posts = posts[::-1]
    event = getHeader(pk)
    return render(request, 'events.html', {'posts': posts, 'event' : event })

def explore(request):
    post_base = Post.objects.all()
    posts = []
    for post in post_base:
        user_model = User.objects.get(username=post.user)
        profile = Profile.objects.get(user=user_model)
        posts.append({'post':post, 'profile': profile})
    posts = posts[::-1]
    return render(request, 'explore.html', {'posts': posts})

@login_required(login_url='login')
def post(request, pk):
    post = Post.objects.get(id=pk)
    user_model = User.objects.get(username=post.user)
    profile = Profile.objects.get(user=user_model)
    return render(request, 'post.html', {'post': post, 'profile': profile})

@login_required(login_url='login')
def profile(request, pk):
    is_me = (pk == request.user.username)
    follow_rel = Follow.objects.filter(following=pk, follower=request.user.username).exists()
    user_object = User.objects.get(username=pk)
    profile = Profile.objects.get(user=user_object)
    posts = Post.objects.all().filter(user=user_object)
    following = len(Follow.objects.filter(follower=pk))
    follower = len(Follow.objects.filter(following=pk))
    return render(request, 'profile.html', {'is_me' : is_me, 'posts': posts, 'profile':profile, 'follow_rel': follow_rel, 'following': following, 'follower': follower})

@login_required(login_url='login')
def createpost(request):
    if request.method == 'POST':
        if request.FILES.get('post_image') == None:
            profile_image = request.FILES.get('post_image')
            title = request.POST.get('title')
            description = request.POST.get('description')
            post_event = request.POST.get('event')
            post = Post(user=request.user, title=title, description=description, post_event=post_event)
            post.save()
        else:
            profile_image = request.FILES.get('post_image')
            title = request.POST.get('title')
            description = request.POST.get('description')
            post_event = request.POST.get('event')
            post = Post(user=request.user, image=profile_image, title=title, description=description, post_event=post_event)
            post.save()
        return redirect('/profile/' + request.user.username )
    return render(request, 'blog/create-post.html')

@login_required(login_url='login')
def editprofile(request):
    profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        if request.FILES.get('profile_image') == None:
            image = profile.profile_picture
            bio = request.POST.get('biotext')
            name = request.POST.get('name')
            profile.profile_picture = image
            profile.bio = bio
            profile.user.first_name = name
            profile.user.save()
            profile.save()
        else:
            image = request.FILES.get('profile_image')
            bio = request.POST.get('biotext')
            name = request.POST.get('name')
            profile.profile_picture = image
            profile.bio = bio
            profile.user.first_name = name
            profile.user.save()
            profile.save()
        return redirect('/profile/'+profile.user.username)
    return render(request, 'editprofile.html', {'profile': profile})

@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.user
        following = request.POST.get('username')
        if Follow.objects.filter(following=following, follower=follower).first():
            delele_follow = Follow.objects.filter(following=following, follower=follower).first()
            delele_follow.delete()
            is_following = False
        else:
            create_follow = Follow(following=following, follower=follower)
            create_follow.save()
            is_following = True

        follower_count = Follow.objects.filter(following=following).count()

        data = {
            'is_following': is_following,
            'follower_count': follower_count
        }
        return JsonResponse(data)

    return HttpResponse("Followed Successfully!!!")

@login_required(login_url='login')
def like(request, pk):
    post = Post.objects.get(id=pk)
    try:
        if Like.objects.filter(post_id=pk, username=request.user).exists():
            del_like = Like.objects.get(post_id=pk, username=request.user.username)
            del_like.delete()
            post.likes = post.likes - 1
            post.save()
        else:
            create_like = Like(post_id=pk, username=request.user.username)
            create_like.save()
            post.likes = post.likes + 1
            post.save()
        return redirect('/')
    except:
        return redirect('home')

@login_required(login_url='login')
def editpost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        if request.FILES.get('post_image') == None:
            post.title = request.POST['title']
            post.description = request.POST['description']
            post.post_event = request.POST['event']
            post.save()
        else:
            post.title = request.POST['title']
            post.description = request.POST['description']
            post.image = request.FILES['post_image']
            post.post_event = request.POST['event']
            post.save()
        return redirect('/profile/'+post.user)
    if post.user != request.user.username:
        return HttpResponse("<h1>Something went wrong</h1>")
    
    return render(request, 'editpost.html', {'post': post})

@login_required(login_url='login')
def deletepost(request, pk):
    post = Post.objects.get(id=pk)
    if post.user != request.user.username:
        return HttpResponse("<h1>You are not allowed to do this!!!</h1>")
    post.delete()
    return redirect('/profile/' + post.user)

def forgetpassword(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        npass = request.POST['npass']
        npass1 = request.POST['npass1']
        error = False
        try:
            user = User.objects.get(username=username, email=email)
            if npass != npass1:
                messages.info(request, "Confirm password not matched!")
                error = True
            if error:
                return redirect('forgetpassword')
            user.set_password(npass)
            user.save()
            return redirect('login')
        except:
            messages.info(request, "User Not Found : )")
            return redirect('forgetpassword')
    return render(request, 'auth/forgetpassword.html')