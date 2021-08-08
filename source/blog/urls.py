from django.urls import path
from blog.views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'blog'
urlpatterns = [
    path("", IndexClass.as_view(), name="index"),
    path("new/",FormClass.as_view(), name="post"),
    path("successful/",PostSuccessfulClass.as_view(), name="post_successful"),
    path("list/",PostList.as_view(),name="list"),
    path("list_detail/<int:pk>/",ListDetail.as_view(),name="list_detail"),
    path("login_successful",LoginSuccessfulClass.as_view(),name="login_successful"),
    path("create/",UserCreateClass.as_view(),name='account_create'),
    path("create_successful/",CreateSuccessClass.as_view(),name='create_success'),
    path("login/",LoginClass.as_view(),name='login'),
    path("connect_logout",ConnectLogoutClass.as_view(),name='connect_logout'),
    path("logout/",LogoutClass.as_view(),name='logout'),
    path("logout_success/",LogoutedClass.as_view(),name='logout_successful'),
    path("list_detail/<int:pk>/edit/",ListEditClass.as_view(),name='list_edit'),
    path("edit_successful/",EditSuccessClass.as_view(),name='edit_successful'),
    path("list_detail/<int:pk>/delete",ListDeleteClass.as_view(),name='list_delete'),
    path("delete_successful/",DeleteSuccessClass.as_view(),name='delete_successful'),
    path("user_page/<int:pk>",UserDetailClass.as_view(),name='user_page'),
    path("another_user_page/<int:pk>/<str:username>",Another_UserDetailClass.as_view(),name='another_user_page'),
    path("category_list",CategoryList.as_view(),name='category_list'),
    path("tag_list",TagList.as_view(),name='tag_list'),
    path("category_detail/<int:pk>",CategoryDetail.as_view(),name='category_detail'),
    path("tag_detail/<int:pk>",TagDetail.as_view(),name='tag_detail'),
    path("category_search/<int:pk>",CategoryDetail.as_view(),name='category_search'),
    path('comment/<int:pk>/', CommentFormView.as_view(), name='comment_form'),
    path('comment/<int:pk>/<str:username>', CommentDeleteView.as_view(), name='delete_comment'),
    path('reply/<int:pk>/', ReplyFormView.as_view(), name='reply_form'),
    path('reply/<int:pk>/<str:username>',ReplyDeleteView.as_view(), name='delete_reply'),
    path('category_entry/', AddCategoryView.as_view(), name='add_category'),
    path('tag_entry/', AddTagView.as_view(), name='add_tag'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)