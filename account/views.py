from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm #로그인,회원가입 폼
from django.contrib.auth import login,logout
from account.forms import RegisterForm
from account.models import CustomUser
from django.contrib import messages

# Create your views here.
def login_view(request):
    if request.method =='POST':
        auth_form = AuthenticationForm(request=request, data = request.POST)
        if auth_form.is_valid():
            v_username = auth_form.cleaned_data.get('username')
            v_password = auth_form.cleaned_data.get('password')
            auth_user = auth.authenticate(request=request, username = v_username, password = v_password)
            login(request, auth_user)
            return redirect('urlnamehome')
        else:
            if CustomUser.objects.filter(username = request.POST['username']).exists():
                messages.info(request, '비밀번호가 일치하지 않습니다.')
                return redirect('urlnamelogin')
            else:
                messages.info(request, '존재하지 않는 계정입니다.')
                return redirect('urlnamelogin')
    
    
    else:
        login_form = AuthenticationForm()
        return render (request, 'login.html', {'views_login_form':login_form})

def signup_view(request):
    if request.method == 'POST':
        new_signup_form = RegisterForm(request.POST)

        if CustomUser.objects.filter(phone_number=request.POST['phone_number']).exists(): #전화번호중복체크
                messages.info(request, '하나의 전화번호로 하나의 계정만 생성할 수 있습니다.')
                return redirect ('urlnamesignup')

        if new_signup_form.is_valid():
            user = new_signup_form.save()
            login(request, user)
            return redirect ('urlnamehome')
        else:
            if CustomUser.objects.filter(username=request.POST['username']).exists(): #id중복체크
                messages.info(request, '중복되는 아이디가 존재합니다.')
                return redirect ('urlnamesignup')
            
            elif request.POST['password1'] != request.POST['password2']: #비밀번호와 비밀번호 확인 다를 때
                messages.info(request, '비밀번호와 비밀번호 확인이 일치하지 않습니다.')
                return redirect ('urlnamesignup')

            elif len(request.POST['password1']) < 8 : #비밀번호가 8자 미만일 때
                messages.info(request, '비밀번호는 8자리 이상으로 작성해주세요.')
                return redirect ('urlnamesignup')

            elif request.POST['password1'].isdigit():
                messages.info(request, '비밀번호는 숫자로만 이루어질 수 없습니다.')
                return redirect ('urlnamesignup')

            elif request.POST['username'] in request.POST['password1']:
                messages.info(request, '비밀번호에 아이디가 포함될 수 없습니다.')
                return redirect ('urlnamesignup')

            elif CustomUser.objects.filter(student_id=request.POST['student_id']).exists(): #학번중복체크
                messages.info(request, '하나의 학번은 하나의 계정만 생성할 수 있습니다.')
                return redirect ('urlnamesignup')
            
            else:
                messages.info(request, '알 수 없는 에러입니다. 관리자 문의.')
                return redirect ('urlnamesignup')
            

      
    else :
        signup_form = RegisterForm()
        return render (request, 'signup.html',{'views_signup_form':signup_form})

def logout_view(request):
    logout(request)
    return redirect('urlnamehome')
