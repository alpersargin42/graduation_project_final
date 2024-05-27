from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from payment.forms import *
from payment.models import *
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart
import random
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


@login_required
def inbox(request):
    messages = request.user.received_messages.all().order_by('-timestamp')
    return render(request, 'inbox.html', {'messages': messages})

@login_required
def sent_messages(request):
    messages = request.user.sent_messages.all().order_by('-timestamp')
    return render(request, 'sent_messages.html', {'messages': messages})


@login_required
def send_message(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    receiver = product.added_by.user

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.product = product
            message.save()
            messages.success(request, 'Mesaj başarıyla gönderildi.')
            return redirect('home')
    else:
        form = MessageForm()

    return render(request, 'send_message.html', {'form': form, 'product': product, 'receiver': receiver})

def product_process(request):
    return render(request, 'product_process.html')

@login_required
def product_list(request):
    if request.user.is_superuser:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(added_by=request.user.profile)
    return render(request, 'product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            try:
                # Kullanıcı ile ilişkili profil kaydını elde ediyoruz
                profile = request.user.profile
                new_product.added_by = profile
                new_product.save()
                messages.success(request, 'Ürün başarıyla eklendi.')
                return redirect('product_list')
            except ObjectDoesNotExist:
                messages.error(request, 'Kullanıcı bir profil ile ilişkilendirilmemiş.')
        else:
            messages.error(request, 'Form geçersiz. Lütfen tekrar deneyin.')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ürün başarıyla güncellendi.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Ürün başarıyla silindi.')
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})


def search(request):
	if request.method == "POST":
		searched = request.POST['searched']
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		if not searched:
			messages.success(request, "Ürün Bulunamadı...")
			return render(request, "search.html", {})
		else:
			return render(request, "search.html", {'searched':searched})
	else:
		return render(request, "search.html", {})	
	
def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		# Get Current User's Shipping Info
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		# Get User's Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)		
		if form.is_valid() or shipping_form.is_valid():
			# Save original form
			form.save()
			# Save shipping form
			shipping_form.save()
			messages.success(request, "Bilgiler Başarıyla Güncellendi!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form,'shipping_form':shipping_form})
	else:
		messages.success(request, "HATA!!")
		return redirect('home')


def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Şifreniz Başarıyla Güncellendi!!")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "HATA!!Şifreniz Güncellenemedi...")
		return redirect('home')

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "Kullanıcı Başarıyla Güncellendi!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "HATA!!Kullanıcı Güncellenemedi...")
		return redirect('home')

def category_summary(request):
        categories = Category.objects.all()

        return render(request, 'category_summary.html', {'categories':categories})
def category(request, foo):
	foo = foo.replace('-', ' ')
	try:
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("Kategori Bulunamadı..."))
		return redirect('home')
def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = Comment.objects.filter(product=product)	
    related_products = list(Product.objects.filter(category=product.category).exclude(id=product.id))
    if len(related_products) > 3:
        related_products = random.sample(related_products, 3)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.product = product
            new_comment.save()
            messages.success(request, 'Yorumunuz başarıyla eklendi.')
            return redirect('product', pk=pk)
        else:
            messages.error(request, 'Yorum eklenirken bir hata oluştu. Lütfen tekrar deneyin.')
    else:
        form = CommentForm()
    return render(request, 'product.html', {'product': product,'related_products': related_products,'comments': comments, 'form': form,})
def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'products':products})

def about(request):
    return render(request,'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
			# Do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
			# Get their saved cart from database
            saved_cart = current_user.old_cart
			# Convert database string to python dictionary
            if saved_cart:
				# Convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
				# Add the loaded cart dictionary to our session
				# Get the cart
                cart = Cart(request)
				# Loop thru the cart and add the items from the database
                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, "Giriş Başarılı...")
            return redirect('home')
        else:
            messages.error(request, "Hata, Tekrar Deneyiniz...")  
            return redirect('login') 
    else:
        return render(request, 'login.html', {})
def logout_user(request):
    logout(request)
    messages.success(request,("Çıkış Başarılı..."))
    return redirect('home')
def register_user(request):
    form=SignUpForm()
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,"Kaydoldunuz..")
            return redirect('update_info')
        else:
            messages.warning(request,("Kayıt Olurken Hata..."))
            return redirect('register')
    
    else:
        return render(request,'register.html',{'form':form})