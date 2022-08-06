from django.shortcuts import redirect, render
from .forms import SigninForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            if cd['username'] and cd['passwword']:
                user = get_user_model().objects.filter(username= cd['username']).first()
                if user is not None:
                    user_auth = authenticate(username = user.username, password = cd['password'])
                    login(request, user_auth)
                    return redirect('farms:farm')
                else:
                    messages.error(request, 'نام کاربری یا پسورد صحیح نمیباشد', 'warning')
                    return redirect('accounts:signin')
            else:
                messages.error(request, 'لطفا فیلدها را پرکنید', 'warning')
                return redirect('accounts:signin')
        else:
            messages.error(request, ' لطفا فیلدها را چک کنید', 'warning')
    else:
        return render(request, 'signin.html', {'form':form})

@login_required
def signout(request):
    logout(request)
    messages.success(request, 'شما با موفقیت از سایت خارج شدید', 'success')
    return redirect('accounts:signin')