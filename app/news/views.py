from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy

from django.core.files.storage import FileSystemStorage

from .models import News, Category, Users_Pands
from .forms import *
from .utils import MyMixin

class HomeNews(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        getLogCookies = {
            'auth': self.request.COOKIES.get('AuthPanda'), 
            'name': self.request.COOKIES.get('NamePanda')
        }
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости корпорации'
        context['auth'] = getLogCookies

        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)

class NewsCategory(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        getLogCookies = {
            'auth': self.request.COOKIES.get('AuthPanda'), 
            'name': self.request.COOKIES.get('NamePanda')
        }
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        context['auth'] = getLogCookies

        return context
        
    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)

class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news'

def RegisterUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            check_Date = form.cleaned_data
            if check_Date['password1'] == check_Date['password2']:
                Users_Pands.objects.create(nickname_user=check_Date['nickname'], name_user=check_Date['name'], surname_user=check_Date['surname'], email_user=check_Date['email'], password_user=check_Date['password1'])
                messages.success(request, 'Вы успешно зарегистрировались')
                
                return redirect('login')
            else: 
                messages.error(request, 'Пароли не совпадают') 
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = RegisterForm()
    
    getLogCookies = {
            'auth': request.COOKIES.get('AuthPanda'), 
            'name': request.COOKIES.get('NamePanda')
    }

    return render(request, 'news/createuser.html', {"form": form, "auth": getLogCookies})

def LoginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            check_Date = form.cleaned_data
            if Users_Pands.objects.filter(nickname_user=check_Date['nickname'], password_user=check_Date['password']):
                messages.success(request, 'Вы успешно авторизовались')
                
                get_name = Users_Pands.objects.get(nickname_user=check_Date['nickname']).name_user
                get_adm = Users_Pands.objects.get(nickname_user=check_Date['nickname']).is_admin_user

                response = redirect('home')
                response.set_cookie('AuthPanda', get_adm, 1000*60*60*24)
                response.set_cookie('NamePanda', get_name, 1000*60*60*24)
                print(get_adm)
                return response
            else: 
                messages.error(request, 'Неправильный логин или пароль') 
            
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = LoginForm()
    
    getLogCookies = {
            'auth': request.COOKIES.get('AuthPanda'), 
            'name': request.COOKIES.get('NamePanda')
    }

    return render(request, 'news/loginuser.html', {"form": form, "auth": getLogCookies})

def QuiteUser(request):
    response = redirect('home')
    response.delete_cookie('AuthPanda')
    response.delete_cookie('NamePanda')
    return response

# ============================================================================= Админ панель
def HomeAdmin(request):
    getLogCookies = {
        'auth': request.COOKIES.get('AuthPanda'), 
        'name': request.COOKIES.get('NamePanda')
    }
    if request.COOKIES.get('AuthPanda') == 'True':
        context = {
            'auth': getLogCookies,
            'title': 'Админ-панель'
        }
        return render(request, 'admin_panel/index.html', context)
    else:
        return redirect('home')

# ~~~~~~~~~~~~ Пользователи ~~~~~~~~~~~~
def CreateUser(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            check_Date = form.cleaned_data
            if check_Date['password1'] == check_Date['password2']:
                Users_Pands.objects.create(nickname_user=check_Date['nickname'], name_user=check_Date['name'], surname_user=check_Date['surname'], email_user=check_Date['email'], password_user=check_Date['password1'], is_admin_user=check_Date['is_admin'])
                messages.success(request, 'Вы успешно создали нового пользователя')
            else: 
                messages.error(request, 'Пароли не совпадают') 
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = CreateUserForm()
    
    getLogCookies = {
            'auth': request.COOKIES.get('AuthPanda'), 
            'name': request.COOKIES.get('NamePanda')
    }

    if request.COOKIES.get('AuthPanda') == 'True':
        context = {
            "form": form,
            "auth": getLogCookies,
            "type": 'create_in_admin',
            "title": 'Создание пользователя',
        }
        return render(request, 'admin_panel/index.html', context)
    else:
        return redirect('home')

class ListUsers(MyMixin, ListView):
    model = Users_Pands
    template_name = 'admin_panel/index.html'
    context_object_name = 'list_admin'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.get_cookie_pands_self(self) != 'redir':
            context = super().get_context_data(**kwargs)
            context['title'] = 'Список пользователей'
            context['auth'] = self.get_cookie_pands_self(self)
            context['type'] = 'list_in_admin'
            context['type_list'] = 'users'
            return context
        else:
            return redirect('home')

class EditUsers(MyMixin, UpdateView):
    model = Users_Pands
    form_class = UpdateUsers
    template_name = 'admin_panel/index.html'
    context_object_name = 'edit_admin'

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.get_cookie_pands_self(self) != 'redir':
            context = super().get_context_data(**kwargs)
            context['title'] = 'Редактирование пользователя'
            context['auth'] = self.get_cookie_pands_self(self)
            context['type'] = 'edit_in_admin'
            return context
        else:
            return redirect('home')

    def form_valid(self, form):
        return self.save_in_view(self, form, 'Вы успешно изменили пользователя', 'admin-panel-listuser')

class DeleteUser(DeleteView):
    model = Users_Pands
    success_url = reverse_lazy('admin-panel-listusers')
    template_name = 'admin_panel/confirm_delete.html'

# ~~~~~~~~~~~~ Новости ~~~~~~~~~~~~
class CreateNews(MyMixin, CreateView):
    form_class = CreateNewsForm
    template_name = 'admin_panel/index.html'
    
    def get_context_data(self, *, object_list=None, **kwargs):
        if self.get_cookie_pands_self(self) != 'redir':
            context = super().get_context_data(**kwargs)
            context['title'] = 'Создание новости'
            context['auth'] = self.get_cookie_pands_self(self)
            context['type'] = 'create_in_admin'
            return context
        else:
            return redirect('home')

    
    def form_valid(self, form):
        return self.save_in_view(self, form, 'Вы успешно создали новую новость', 'admin-panel')

class ListNews(MyMixin, ListView):
    model = News
    template_name = 'admin_panel/index.html'
    context_object_name = 'list_admin'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.get_cookie_pands_self(self) != 'redir':
            context = super().get_context_data(**kwargs)
            context['title'] = 'Список новостей'
            context['auth'] = self.get_cookie_pands_self(self)
            context['type'] = 'list_in_admin'
            context['type_list'] = 'news'
            return context
        else:
            return redirect('home')

class EditNews(MyMixin, UpdateView):
    model = News
    form_class = UpdateNews
    template_name = 'admin_panel/index.html'
    context_object_name = 'edit_admin'

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.get_cookie_pands_self(self) != 'redir':
            context = super().get_context_data(**kwargs)
            context['title'] = 'Редактирование новости'
            context['auth'] = self.get_cookie_pands_self(self)
            context['type'] = 'edit_in_admin'
            return context
        else:
            return redirect('home')

    def form_valid(self, form):
        return self.save_in_view(self, form, 'Вы успешно изменили новость', 'admin-panel-listnews')

class DeleteNews(DeleteView):
    model = News
    success_url = reverse_lazy('admin-panel-listnews')
    template_name = 'admin_panel/confirm_delete.html'

# ~~~~~~~~~~~~ Категории ~~~~~~~~~~~~
class CreateCategory(MyMixin, CreateView):
    form_class = CreateCategoryForm
    template_name = 'admin_panel/index.html'

    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.get_cookie_pands_self(self) != 'redir':
            context = super().get_context_data(**kwargs)
            context['title'] = 'Создание категории'
            context['auth'] = self.get_cookie_pands_self(self)
            context['type'] = 'create_in_admin'
            return context
        else:
            return redirect('home')
    
    def form_valid(self, form):
        return self.save_in_view(self, form, 'Вы успешно создали новую категорию', 'admin-panel')
        
class ListCategory(MyMixin, ListView):
    model = Category
    template_name = 'admin_panel/index.html'
    context_object_name = 'list_admin'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.get_cookie_pands_self(self) != 'redir':
            context = super().get_context_data(**kwargs)
            context['title'] = 'Список категорий'
            context['auth'] = self.get_cookie_pands_self(self)
            context['type'] = 'list_in_admin'
            context['type_list'] = 'category'
            return context
        else:
            return redirect('home')

class EditCategory(MyMixin, UpdateView):
    model = Category
    form_class = UpdateCategory
    template_name = 'admin_panel/index.html'
    context_object_name = 'edit_admin'

    def get_context_data(self, *, object_list=None, **kwargs):
        if self.get_cookie_pands_self(self) != 'redir':
            context = super().get_context_data(**kwargs)
            context['title'] = 'Редактирование категории'
            context['auth'] = self.get_cookie_pands_self(self)
            context['type'] = 'edit_in_admin'
            return context
        else:
            return redirect('home')

    def form_valid(self, form):
        return self.save_in_view(self, form, 'Вы успешно изменили категорию', 'admin-panel-listcategory')

class DeleteCategory(DeleteView):
    model = Category
    success_url = reverse_lazy('admin-panel-listcategory')
    template_name = 'admin_panel/confirm_delete.html'

