from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
	shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ad Soyad'}), required=True)
	shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Adresi'}), required=True)
	shipping_address1 = forms.CharField(label="Ev Adresim", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ev Adresim'}), required=True)
	shipping_address2 = forms.CharField(label="İş Adresim", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'İş Adresim'}), required=False)
	shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Şehir'}), required=True)
	shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'İlçe'}), required=False)
	shipping_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Posta Kodu'}), required=False)
	shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ülke'}), required=True)
	# ev_or_is = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nereye Gönderilsin'}), required=True)
	ev_or_is = forms.ChoiceField(label="Nereye Gönderilsin", choices=[('Ev Adresi', 'Ev Adresim'), ('İş Adresi', 'İş Adresim')], widget=forms.RadioSelect, required=True)

	class Meta:
		model = ShippingAddress
		fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country', 'ev_or_is']

		exclude = ['user',]

class PaymentForm(forms.Form):
	card_name =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Kredi Kartı Adı Soyadı'}), required=True)
	card_number =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Kart Numarası'}), required=True)
	card_exp_date =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Son Kullanım Tarihi'}), required=True)
	card_cvv_number =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV Kodu'}), required=True)