import hashlib
import uuid

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from pyecharts import Bar

from webpro.models import User, Admin, Jobinfo


# 功能函数部分

def make_token():
    # 刚生成的token其实是128,默认进行了进制转换,转换为了16进制
    token = str(uuid.uuid4())

    md55 = hashlib.md5()
    md55.update(token.encode('utf-8'))
    token = md55.hexdigest()

    return token











# 视图函数部分

def get_jobinfo(request):
    job_name_dict ={}
    jobinfos = Jobinfo.objects.all()
    for jobinfo in jobinfos:
        job_name = jobinfo.jobname

        if job_name not in job_name_dict.keys():
            job_name_dict[job_name] = 1

        else:
            job_name_dict[job_name] += 1


    #构建柱状图
    attr = job_name_dict.kyes()
    v1 = job_name_dict.values()
    bar = Bar('各职位在招统计图')
    bar.add("智联招聘", attr, v1, is_stack=True)
    return render(request,'get_jobinfo.html',context={'key':key})


def home_page(request):
    return render(request,'home_page.html')


def register(request):
    return render(request,'register.html')


def save_user(request):
    u_username = request.POST.get('u_username')
    u_password = request.POST.get('u_password')
    u_phone = request.POST.get('u_phone')
    u_email = request.POST.get('u_email')

    user = User()

    user.u_username = u_username
    user.u_password = u_password
    user.u_email = u_email
    user.u_phone = u_phone
    u_token = make_token()
    user.u_token = u_token

    user.save()

    #保存完注册信息之后跳转到注册成功页面
    response = HttpResponseRedirect(reversed("webpro:register_success"))
    response.set_cookie('u_token',u_token)

    return response


def register_success(request):
    #拿到服务器传过来的token
    u_token = request.COOKIES.get('u_token')

    if u_token:
        users = User.objects.filter(u_token=u_token)
        if users.exists():
            user = users.filter()

    return render(request,'register_success.html',context={'user':user})


def login_user(request):
    data = {
        'statu': '200',
    }
    u_username = request.POST.get('u_username')
    u_password = request.POST.get('u_password')

    # 创建一个返回对象
    response = render(request, 'home_page.html', context=data)

    users = User.objects.filter(u_username=u_username)

    if users.exists():
        user = users.first()
        if u_password == user.u_password:
            u_token = make_token()
            user.u_token = u_token
            user.save()

            # 为返回对象设置token
            response.set_cookie('u_token', u_token)

            data['u_username'] = u_username
        else:
            data['statu']='401'
    else:
        data['statu']= '401'

    return response


def login_admin(request):
    data = {
        'statu': '200',
    }
    a_username = request.POST.get('a_username')
    a_password = request.POST.get('a_password')

    admins = Admin.objects.filter(a_username=a_username)

    if admins.exists():
        admin = admins.first()
        if a_password == admin.a_password:
            data['a_username'] = a_username
        else:
            data['statu'] = '401'
    else:
        data['statu'] = '401'

    return render(request, 'home_page.html', context=data)
