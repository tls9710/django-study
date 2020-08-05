from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Account

# Create your views here.

def signup(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')

        if user_id =="" or nickname =="" or email =="" or pw1 == "" or pw2 == "":
            messages.info(request, "모든 항목을 채워주세요")
            return redirect('signup')

        if not pw1 == pw2:
            messages.info(request, "비밀번호가 다릅니다.")
            return redirect('signup')

        user = User.objects.create_user(username = user_id, password = pw1)
        user.save()
        account = Account(user=user, email=email, nickname=nickname)
        account.save()
        return redirect('login')
    else:
        return render(request, 'signup.html')
    return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        username = request.POST['id']
        password = request.POST["password"]

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, "회원정보가 일치하지 않습니다.")
            return redirect('login')
    else:
        return render(request, 'login.html')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')



def id_overlap_check(request):
    username = request.GET.get('username')
    try:
        #중복 검사 실패
        user = User.objects.get(username=username)
    except:
        #중복 검사 성공
        user = None
    if user is None:
        overlap = "pass"
    else:
        overlap = "fail"
    context = {'overlap' : overlap}
    return JsonResponse(context)