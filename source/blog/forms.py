from django.contrib.auth import forms as auth_forms
from django import forms
from .models import Post,CommentPost,ReplyPost,Category,Tag
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model


class CreateForm(UserCreationForm):
    class Meta:
        User = get_user_model()
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

class PostList(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('tags','category','content','title','description','username','image')
        widgets = {
        'content':forms.Textarea(attrs={'rows':30,'cols':100,'placeholder':'本文の入力'}),
        'description':forms.Textarea(attrs={'rows':30,'cols':100,'placeholder':'備考、その他'}),
        'title':forms.Textarea(attrs={'rows':1,'cols':50,'placeholder':'タイトルを255文字以内で入力'}),
        'username':forms.Textarea()
         }

class CommentForm(forms.ModelForm):

    class Meta:
        model = CommentPost
        fields = ('name','content')
        widgets = {
            'name': forms.TextInput(attrs={
                'class':  'form-control',
                'placeholder':'名前',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder':'本文',
            }),
        }
        labels = {
            'name':'',
            'content':'',
        }
class ReplyForm(forms.ModelForm):

    class Meta:
        model = ReplyPost
        fields = ('name','content')
        widgets = {
            'name': forms.TextInput(attrs={
                'class':  'form-control',
                'placeholder':'名前',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder':'本文',
            }),
        }
        labels = {
            'name':'',
            'content':'',
        }

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'カテゴリを入力',
            }),

        }
        labels = {
            'name': '',

        }

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'タグを入力',
            }),

        }
        labels = {
            'name': '',

        }