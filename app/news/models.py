from email.policy import default
from django.db import models
from django.urls import reverse

# id
# title
# content
# created_at
# updated_at
# photo
# is_published
# category

class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название поста')
    content = models.TextField(blank=True, verbose_name='Описание новости')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновление')
    photo = models.ImageField(upload_to='uploads/%Y/%m/%d', verbose_name='Фотография поста', blank=True)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.SET_DEFAULT, verbose_name='Категория', blank=True, default="")

    def get_url_show(self):
        return reverse('view_news', kwargs={"pk": self.pk})

    def get_url_edit(self):
        return reverse('admin-panel-editnews', kwargs={"pk": self.pk})
    
    def get_url_deletes(self):
        return reverse('admin-panel-deletenews', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='Новости'
        ordering = ['-created_at']

class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Название категорий')

    def get_url_show(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def get_url_edit(self):
        return reverse('admin-panel-editcategory', kwargs={"pk": self.pk})
    
    def get_url_deletes(self):
        return reverse('admin-panel-deletecategory', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name='Категории'
        ordering = ['id']

class Users_Pands(models.Model):
    nickname_user = models.CharField(max_length=150, verbose_name='Название пользователя')
    name_user = models.CharField(max_length=100, verbose_name='Имя пользователя')
    surname_user = models.CharField(max_length=100, verbose_name='Фамилия пользователя')
    email_user = models.EmailField(verbose_name='Почта пользователя')
    password_user = models.CharField(max_length=100, verbose_name='Пароль пользователя')
    is_admin_user = models.BooleanField(blank=True, default=False, verbose_name='Администратор')

    def get_url_edit(self):
        return reverse('admin-panel-edituser', kwargs={"pk": self.pk})
    
    def get_url_deletes(self):
        return reverse('admin-panel-deleteuser', kwargs={"pk": self.pk})

    def __str__(self):
        return self.nickname_user

    class Meta:
        verbose_name = 'Пользователи Панды'
        ordering = ['id']
