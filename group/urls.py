# group/urls.py

from django.urls import path
from . import views



urlpatterns = [
    # مسیر برای ایجاد گروه
    path('create/', views.CreateGroup.as_view(), name='create_group'),

    path('edit/', views.GroupEdit.as_view(), name='edit_group'),

    # مسیر برای مشاهده لیست گروه‌ها
    path('list/', views.GroupList.as_view(), name='group_list'),

    # مسیر برای مشاهده جزئیات یک گروه خاص
    path('detail/<int:pk>/', views.GroupDetail.as_view(), name='group_detail'),

    # مسیر برای مشاهده اعضای یک گروه خاص
    path('members/<int:group_id>/', views.GroupMembersList.as_view(), name='group_members'),

    # مسیر برای اضافه کردن عضو به گروه
    path('add_member/<int:group_id>/', views.AddGroupMember.as_view(), name='add_group_member'),

    path('add_image/', views.AddGroupImage.as_view(), name='add_group_image'),

    # مسیر برای اضافه کردن تصویر به گالری گروه

    path('<int:group_id>/gallery/', views.GroupGalleryListView.as_view(), name='group-gallery'),

    path('<int:group_id>/gallery/upload/', views.GroupGalleryUploadView.as_view()),
    
    path('<int:group_id>/gallery/<int:image_id>/delete/', views.GroupGalleryDeleteView.as_view()),
]
