from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm
from django import forms
from .models import *

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'is_sale', 'sale_price', 'price']


class UserInfoForm(forms.ModelForm):
	phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Telefon'}), required=False)
	address1 = forms.CharField(label="Ev Adresim", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ev Adresim'}), required=False)
	address2 = forms.CharField(label="İş Adresim", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'İş Adresim'}), required=False)
	city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Şehir'}), required=False)
	state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'İlçe'}), required=False)
	zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Posta Kodu'}), required=False)
	country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ülke'}), required=False)

	class Meta:
		model = Profile
		fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', )


class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Şifre'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Şifreler uyuşmalı...</li><li>Şifreniz en az 8 karakter olmalı...</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Şifrenizi Onaylayınız'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Doğrulama için öncekiyle aynı şifre olmalı...</small></span>'

class UpdateUserForm(UserChangeForm):
	password=None
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Adresiniz'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adınız'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Soyadınız'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Kullanıcı Adı'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>150 karakterden az veya eşit olmalıdır. Sadece harf, rakam ve @/./+/-/_ karakterleri kullanılabilir.</small></span>'

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Adresiniz'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adınız'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Soyadınız'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'Kullanıcı Adı'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>150 karakterden az veya eşit olmalıdır. Sadece harf, rakam ve @/./+/-/_ karakterleri kullanılabilir.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Şifre'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Şifreler uyuşmalı...</li><li>Şifreniz en az 8 karakter olmalı...</li></ul>'
		#<li>Şifreniz sık kullanılan bir şifre olamaz...</li><li>Şifreniz tamamen sayısal olamaz...</li>

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Şifrenizi Onaylayınız'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Doğrulama için öncekiyle aynı şifre olmalı...</small></span>'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'title', 'rating', 'comment']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'İsim Soyisim'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Başlık'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Yorumunuz'}),
        }