from django import forms
from users.models import CustomUser


#LOGIN form
class UserLoginForm(forms.ModelForm):
   class Meta:
       model = CustomUser
       fields = ('username','password')
       widgets = {
           "username": forms.TextInput(attrs={'placeholder': 'Username'}),
           "password": forms.TextInput(attrs={'placeholder': 'Parol'}),
       }


   def clean(self):
       cleaned_data = super().clean()
       username  = self.cleaned_data['username']
       password = self.cleaned_data['password']
       if username:
           # Foydalanuvchi nomini kichik harflarga aylantiramiz
           cleaned_data['username'] = username.lower()
       return cleaned_data



#END login form


class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Yangi Parol')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Parolni takrorlang')
    class Meta:
        model = CustomUser
        fields = ("username",  "password", "password2")

    def clean_username(self):
        # Username ni kichkina harfga aylantirib keyin tekshirish
        username = self.cleaned_data['username'].lower()
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Bu username band. iltimos boshqasini tanlang.')
        return username


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError('Parollar bir birga mos emas')


        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

# -*-  EDIT  -*-
class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','picture','bio']


#Password change form
class PasswordChangeForm(forms.ModelForm):
    passwordold = forms.CharField(widget=forms.PasswordInput(), label='Joriy parolni kiriting')
    password = forms.CharField(widget=forms.PasswordInput(), label='Yangi Parol')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Parolni takrorlang')

    class Meta:
        model = CustomUser
        fields = ['passwordold','password','password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError('Parollar bir birga mos emas')


        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


