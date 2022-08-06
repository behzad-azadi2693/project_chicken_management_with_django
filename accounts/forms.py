from django import forms
from django.contrib.auth import get_user_model
from django.forms import fields
from django.contrib.auth.forms import ReadOnlyPasswordHashField


messages = {
    'required':'این فیلد الزامی است',
    'invalid':'این فیلد صحیح نمیباشد',
    'max_length':'اندازه فیلد بیشتر از حد مجاز',
    'min_length':'اندازه فیلد کمتر از حد مجاز',
}


class SigninForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].error_messages = messages

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
    
class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='پسورد', widget=forms.PasswordInput)
    password_confierm = forms.CharField(label='تکرار پسورد', widget=forms.PasswordInput)

    class Meta:
        models = get_user_model()
        fields = ('username', 'password', 'password_confierm')

    def clean_password_confierm(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password_confierm'] and cd['password'] != cd['password_confierm']:
            raise forms.ValidationError("پسورد و تکرار پسورد یکسان نیست")

        return cd['password_confierm']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        models = get_user_model()
        fields = ('username', 'password')

    def clean_password(self):
        return self.initial['password']