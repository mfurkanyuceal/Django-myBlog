from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from .models import UserProfile


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email):
            raise forms.ValidationError('Bu mail adresi zaten kullanılıyor!')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username):
            raise forms.ValidationError('Bu kullanıcı adı zaten kullanılıyor!')
        return username


class UserProfileForm(forms.ModelForm):
    MAN = 'E'
    FEMALE = 'K'
    OTHER = 'O'

    SEX = {(MAN, 'Erkek'), (FEMALE, 'Kadın'), (OTHER, 'Diğer')}

    sex = forms.CharField(widget=forms.Select(choices=SEX), label='Cinsiyet')
    biography = forms.CharField(widget=forms.Textarea, max_length=500, label='Hakkımda', required=False)
    birth_date = forms.DateField(
        widget=DatePickerInput(format='%d/%m/%Y')
    )
    phone = forms.CharField(max_length=11, label='Telefon Numarası', required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date', 'phone', 'sex', 'biography']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

        self.fields['biography'].widget.attrs['rows'] = 10
        self.fields['biography'].widget.attrs['cols'] = 50


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}


class LoginForm(forms.Form):
    username = forms.CharField(max_length=80, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=80, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']

        if '@' in username:
            if '.com' in username:
                user = User.objects.filter(email=username)
                if len(user) == 1:
                    user = user.first()
                    return user.username
                elif len(user) > 1:
                    raise forms.ValidationError('Lütfen Kullanıcı adınızı giriniz.')
                else:
                    raise forms.ValidationError('Böyle bir kullanıcı bulunamadı!')

        return username


class UserProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_photo']
