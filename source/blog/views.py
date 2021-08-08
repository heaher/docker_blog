from django.shortcuts import render
from blog.models import Post,Tag,Category,CommentPost,ReplyPost
from django.views.generic import ListView, CreateView,TemplateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.db.models import Q,Count
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm,CommentForm,ReplyForm,CategoryForm,TagForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostList,CreateForm
from django import forms
from django.http import Http404
from .models import User
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required



class FormClass(LoginRequiredMixin,CreateView):
    template_name = 'blog/post.html'
    form_class = PostList
    model = User
    success_url = reverse_lazy('blog:post_successful')

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['initial'] = {'username': self.request.user}
        return form_kwargs



class IndexClass(ListView):
    template_name = 'blog/index.html'
    model = Post
    paginate_by = 3


class PostSuccessfulClass(TemplateView):
    template_name = 'blog/post_successful.html'

class PostList(ListView):
    template_name = 'blog/list.html'
    model = Post
    paginate_by = 3
    def get_queryset(self):
        q_word = self.request.GET.get('query')
        print(q_word)

        if q_word:
            object_list = Post.objects.filter(
                title__icontains=q_word)
        else:
            object_list = Post.objects.all()
        return object_list

class ListDetail(DetailView):
    model = Post
    template_name = 'blog/list_detail.html'


class LoginSuccessfulClass(TemplateView):
    template_name = 'blog/login_successful.html'

class UserCreateClass(CreateView):
    form_class = CreateForm
    template_name = 'blog/account_create.html'
    success_url = reverse_lazy('blog:create_success')

class CreateSuccessClass(TemplateView):
    template_name = 'blog/create_success.html'

class LoginClass(LoginView):
    template_name = 'blog/login.html'
    form_class = LoginForm

class ConnectLogoutClass(LoginRequiredMixin, TemplateView):
    template_name = "blog/connect_logout.html"

class LogoutClass(LoginRequiredMixin, LogoutView):
    template_name = "blog/logout.html"

class LogoutedClass(TemplateView):
    template_name = "blog/logout_successful.html"

class ListEditClass(LoginRequiredMixin,UpdateView):
    template_name = 'blog/list_edit.html'
    model = Post
    fields = ['tags', 'category', 'content', 'title', 'description','image']
    success_url = reverse_lazy('blog:edit_successful')

    def get_form(self):
        form = super(ListEditClass, self).get_form()
        form.fields['content'].widget = forms.Textarea(attrs={'rows':30,'cols':100,'placeholder':'本文の入力'})
        form.fields['description'].widget = forms.Textarea(attrs={'rows':30,'cols':100,'placeholder':'備考、その他'})
        form.fields['title'].widget = forms.Textarea(attrs={'rows':1,'cols':50,'placeholder':'タイトルを255文字以内で入力'})

        return form

class EditSuccessClass(TemplateView):
    template_name = 'blog/edit_successful.html'

class ListDeleteClass(LoginRequiredMixin,DeleteView):
    template_name = 'blog/list_delete.html'
    model = Post
    success_url = reverse_lazy('blog:delete_successful')


class DeleteSuccessClass(TemplateView):
    template_name = 'blog/delete_successful.html'

class UserDetailClass(LoginRequiredMixin,ListView):
    template_name = 'blog/user_page.html'
    model = Post
    def get_queryset(self):
        q_word = self.request.GET.get('query')
        print(q_word)

        if q_word:
            object_list = Post.objects.filter(
                title__icontains=q_word)
        else:
            object_list = Post.objects.all()
        return object_list

class Another_UserDetailClass(ListView):
    template_name = 'blog/another_user_page.html'
    model = Post
    def get_queryset(self):
        q_word = self.request.GET.get('query')
        print(q_word)

        if q_word:
            object_list = Post.objects.filter(
                title__icontains=q_word)
        else:
            object_list = Post.objects.all()
        return object_list

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['username'] = self.kwargs.get('username')
        print(context)
        return context

class CategoryList(ListView):
    template_name = 'blog/category_list.html'
    model = Category

    def get_queryset(self):
        q_word = self.request.GET.get('query')
        print(q_word)
        print(self.queryset)
        if q_word:
            object_list = Category.objects.filter(
                name__icontains=q_word).annotate(
            num_posts=Count('post'))
        else:
            object_list = Category.objects.annotate(
            num_posts=Count('post'))
        return object_list



class TagList(ListView):
    template_name = 'blog/tag_list.html'
    model = Tag

    def get_queryset(self):
        q_word = self.request.GET.get('query')
        print(q_word)
        print(self.queryset)
        if q_word:
            object_list = Tag.objects.filter(
                name__icontains=q_word).annotate(
                num_posts=Count('post'))
        else:
            object_list = Tag.objects.annotate(
                num_posts=Count('post'))
        return object_list



class CategoryDetail(DetailView):
    template_name = 'blog/category_detail.html'
    model = Category



class TagDetail(DetailView):
    template_name = 'blog/tag_detail.html'
    model = Tag


class CommentFormView(CreateView):
    model = CommentPost
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_pk = self.kwargs['pk']
        comment.post = get_object_or_404(Post, pk=post_pk)
        comment.save()
        return redirect('blog:list_detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['pk']
        context['post'] = get_object_or_404(Post, pk=post_pk)
        return context



class CommentDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'blog/delete_comment.html'
    model = CommentPost

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        comment_pk = self.kwargs['pk']
        comment = get_object_or_404(CommentPost, pk=comment_pk)
        comment.delete()
        return redirect('blog:list_detail',pk=comment.post.pk)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['username'] = self.kwargs.get('username')
        print(context)
        return context


class ReplyFormView(CreateView):
    model = ReplyPost
    form_class = ReplyForm
    template_name = 'blog/reply_form.html'

    def form_valid(self, form):
        reply = form.save(commit=False)
        comment_pk = self.kwargs['pk']
        print(self.kwargs)
        reply.comment = get_object_or_404(CommentPost, pk=comment_pk)
        reply.save()
        return redirect('blog:list_detail', pk=reply.comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['pk']
        context['comment'] = get_object_or_404(CommentPost, pk=comment_pk)
        return context

class ReplyDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'blog/delete_reply.html'
    model = ReplyPost

    def delete(self, request, *args, **kwargs):
        reply_pk = self.kwargs['pk']
        reply = get_object_or_404(ReplyPost, pk=reply_pk)
        reply.delete()
        return redirect('blog:list_detail', pk=reply.comment.post.pk)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['username'] = self.kwargs.get('username')
        print(context)
        return context


class AddCategoryView(LoginRequiredMixin,CreateView):
    template_name = 'blog/add_category.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('blog:category_list')

class AddTagView(LoginRequiredMixin,CreateView):
    template_name = 'blog/add_tag.html'
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('blog:tag_list')
