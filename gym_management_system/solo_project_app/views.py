from django.shortcuts import render, redirect
from .models import User, Role, Subscription,Class,Admin
from django.contrib import messages
from datetime import date, timedelta
import bcrypt
import secrets
import string
from time import gmtime, strftime
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def index(request):
    if request.session.get('username') != 'admin':
            return redirect('/')
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users')

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('dateofbirth')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        photo = request.FILES.get('photo')
        password = generate_random_password()
        # password = request.POST.get('password')
        # confirm_password = request.POST.get('confirm_password')


        # # Check if passwords match
        # if password != confirm_password:
        #     messages.error(request, "Passwords do not match.")
        #     return redirect('/')

        # pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # Create User
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            dateofbirth=date_of_birth,
            phone_number=phone_number,
            email=email,
            password=password,
            photo = photo,
        )
        request.session['first_name'] = first_name

        # Handle role
        role_title = request.POST.get('role')
        custom_role = request.POST.get('custom_role')
        custom_description = request.POST.get('custom_description')

        if role_title == 'custom' and custom_role:
            role = Role.objects.create(
                title=custom_role,
                description=custom_description,
                user=user
                
            )
        elif role_title == 'member':
            role = Role.objects.create(
                title=role_title,
                description='this is a member',
                user=user
            )
        elif role_title == 'trainer':
            role = Role.objects.create(
                title=role_title,
                description='this is a trainer',
                user=user
            )
        return redirect('/users')

    content = {
        'roles': Role.objects.all(),
        'users': User.objects.all()
    }
    return render(request, 'index.html', content)

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        users = User.objects.filter(email=email)
        if users.exists():
            user = users.first()
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                request.session['userid'] = user.id
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                return redirect('/dashboard')
            messages.error(request, "Incorrect password.")
        else:
            messages.error(request, "User does not exist.")
        return redirect("users")
    return render(request, 'login.html')

def subscriptions(request):
    if request.session.get('username') != 'admin':
            return redirect('/')
    ## mesh jahizzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
    context = {
        'users' : User.objects.all(),
        'roles': Role.objects.all(),
        'subscriptions' : Subscription.objects.all(),
        "time": strftime("%Y-%m-%d %H:%M %p", gmtime()),
        
    }
    return render(request,'subscriptions.html',context)

def add_subscription(request, id):
    if request.session.get('username') != 'admin':
            return redirect('/')
    start_date =  date.today()
    end_date = start_date + timedelta (days = 30)
    Subscription.objects.create(start_date = start_date , end_date = end_date, user = User.objects.get(id = id))
    return redirect('/subscriptions')

def classes(request):
    if request.session.get('username') != 'admin':
            return redirect('/')
    all_classes = Class.objects.all()
    class_data = []
    members = User.objects.filter(roles__title='member') 
    trainers = User.objects.filter(roles__title='trainer') 

    for a_class in all_classes:
        current_size = a_class.users.filter(roles__title='member').count()
        max_size = a_class.max_size
        percentage = (current_size / max_size) * 100 if max_size > 0 else 0  # Avoid division by zero
        
        class_data.append({
            'class': a_class,
            'current_size': current_size,
            'max_size': max_size,
            'percentage': percentage
        })

    content = {
        'roles': Role.objects.all(),
        'users': User.objects.all(),
        'members': members,  # Use members here
        'classes': class_data,
        'trainers':trainers
        
    }

    return render(request, 'classes.html', content)


    
def add_class(request):
    if request.session.get('username') != 'admin':
            return redirect('/')
    title_from_form = request.POST.get('title')
    description_from_form = request.POST.get('description')
    max_size_from_form = request.POST.get('max_size')
    user_id_from_form = request.POST.get('trainer')
    class_id_from_form = request.POST.get('class_id')
    
    a_class = Class.objects.create(
        title=title_from_form,
        description=description_from_form,
        max_size=max_size_from_form
    )
    user = User.objects.get(id=user_id_from_form)
    user.classes.add(a_class)
    
    return redirect('/classes')
        

def user_profile(request, id):
    if request.session.get('username') != 'admin':
            return redirect('/')

    user = get_object_or_404(User, id = id)
    
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)


def update_profile(request, id):
    if request.session.get('username') != 'admin':
            return redirect('/')
    user = get_object_or_404(User, pk=id)
    
    if request.method == 'POST':
   
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('dateofbirth')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        medical_history = request.POST.get('medical_history')
        address = request.POST.get('address')
        photo = request.FILES.get('photo')  # Handling the photo upload
        
        if not first_name or not last_name or not email:
            messages.error(request, 'Please fill in the required fields.')
            return render(request, 'update_profile.html', {'user': user})
        
        # Update the user instance
        user.first_name = first_name
        user.last_name = last_name
        user.dateofbirth = date_of_birth
        user.phone_number = phone_number
        user.email = email
        user.medical_history = medical_history
        user.address = address
        
        if photo:
            user.photo = photo
        
        user.save()
        
        # Show success message and redirect
        messages.success(request, 'Profile updated successfully!')
        return redirect(f"/user/{id}/profile")
    
    return render(request, 'update_profile.html', {'user': user})

def trainers_view(request):
    if request.session.get('username') != 'admin':
            return redirect('/')
    if request.method == 'POST':
        pass
    context = {
    'trainers': User.objects.filter(roles__title='trainer'),
    'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request,'trainers_view.html',context)

def add_user_to_class(request):
    if request.session.get('username') != 'admin':
            return redirect('/')
    if request.method == 'POST':
        member_id_from_form = request.POST.get('member')
        class_id_from_form = request.POST.get('class')
        
        # Get the User and Class objects
        member = User.objects.get(id=member_id_from_form)
        a_class = Class.objects.get(id=class_id_from_form)
        
        # Add the member to the class
        a_class.users.add(member)
        
        # Save the changes
        a_class.save()
        
        return redirect('/classes')
    return render(request, 'classes.html')
def trainer_search(request):
    query = request.GET.get('q')
    trainers = User.objects.all()

    if query:
        trainers = trainers.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(specialties__title__icontains=query)
        ).distinct()

    return render(request, 'trainer_list.html', {'trainers': trainers})

def members_view(request):
    if request.session.get('username') != 'admin':
            return redirect('/')
    if request.method == 'POST':
        pass
    context = {
        'members' : User.objects.filter(roles__title='member'),
        'roles': Role.objects.all(),
        'subscriptions' : Subscription.objects.all(),
    }
    return render(request,'members_view.html',context)

def update_trainer(request):
    if request.session.get('username') != 'admin':
            return redirect('/')
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        trainer_id = request.POST.get('trainer_id')

        cls = get_object_or_404(Class, id=class_id)
        trainer = get_object_or_404(User, id=trainer_id) if trainer_id != 'custom' else None

        # Update the class's trainer
        cls.trainer = trainer
        cls.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def homepage(request):
    if request.session.get('username') == 'admin':
            return redirect('/aboutus')
    if request.method == "POST":
        errors = Admin.objects.basic_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        
        # At this point, we know there are no errors, so login is successful
        user_name_from_form = request.POST.get('username')
        request.session['username'] = user_name_from_form
        return redirect('/aboutus')
        
    return render(request, 'homepage.html')



def logout(request):
    request.session.flush()
    return redirect('/')

def edit_class(request, id):
    class_instance = Class.objects.get(id=id)
    users = User.objects.all()
    roles = Role.objects.all()
    trainers = User.objects.filter(roles__title='trainer')
    members = User.objects.filter(roles__title='member')

    if request.method == 'POST':
        # Handle form submission to update class
        title = request.POST.get('title')
        max_size = request.POST.get('max_size')
        description = request.POST.get('description')
        selected_trainers = request.POST.getlist('trainers')  # Get selected trainer IDs from the form

        class_instance.title = title
        class_instance.max_size = max_size
        class_instance.description = description
        class_instance.save()

        # Update trainers
        class_instance.users.set(User.objects.filter(id__in=selected_trainers))

        return redirect('some_view_name')  # Redirect after saving changes

    # Get current trainers for the class
    current_trainer_ids = class_instance.users.filter(roles__title='trainer').values_list('id', flat=True)

    context = {
        'class': class_instance,
        'users': users,
        'roles': roles,
        'trainers': trainers,
        'members': members,
        'current_trainer_ids': current_trainer_ids,
    }
    return render(request, 'edit_class.html', context)

def aboutus(request):
    return render(request,'aboutus.html')