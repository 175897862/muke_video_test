# conding:utf-8

from django.views.generic import View
from app.libs.base_render import render_to_response
from django.shortcuts import redirect, reverse
from django.contrib.auth import login, logout, authenticate  # 登录，注销，用户名密码验证
from django.contrib.auth.models import User
from django.core.paginator import Paginator  # 分页模块
from app.utils.permission import dashboard_auth


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:  # 判断如果用户已登录，则直接跳转到主页
            return redirect(reverse('dashboard_index'))

        to = request.GET.get('to', '')
        data = {'error': '', 'to': to}
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        to = request.GET.get('to', '')

        data = {}

        exists = User.objects.filter(username=username).exists()
        if not exists:
            data['error'] = '不存在该用户'
            return render_to_response(request, self.TEMPLATE, data=data)

        user = authenticate(username=username, password=password)  # 用户名密码验证
        if not user:
            data['error'] = '密码错误'
            return render_to_response(request, self.TEMPLATE, data=data)

        if not user.is_superuser:
            data['error'] = '你无权登录'
            return render_to_response(request, self.TEMPLATE, data=data)

        login(request, user)  # 完成登录
        if to:
            return redirect(to)

        return redirect(reverse('dashboard_index'))


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


class AdminManager(View):
    TEMPLATE = 'dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):
        # users = User.objects.filter(is_superuser=True)  # 获取管理员集合
        users = User.objects.all()  # 获取所有用户名单

        page = request.GET.get('page', 1)  # 获取当前页数
        p = Paginator(users, 2)  # 按每页显示2个用户进行分页
        total_page = p.num_pages  # 获取分页后的页面总数
        if int(page) <= 1:
            page = 1
        current_page = p.get_page(int(page)).object_list  # 当前页用户列表

        data = {'users': current_page, 'total': total_page, 'page_num': int(page)}
        return render_to_response(request, self.TEMPLATE, data=data)


class UpdateAdminStatus(View):
    def get(self, request):
        status = request.GET.get('status', 'on')

        _status = True if status == 'on' else False
        request.user.is_superuser = _status
        request.user.save()

        return redirect(reverse('admin_manager'))
