from django.urls import path
from . import views

urlpatterns = [
    # چت خصوصی با گروه
    path('private/<int:group_id>/send/', views.SendPrivateMessage.as_view(), name='send_private_message'),
    path('private/<int:group_id>/messages/', views.GetPrivateMessages.as_view(), name='get_private_messages'),

    # چت عمومی تور
    path('tour/<int:tour_id>/chat/send/', views.SendTourChatMessage.as_view(), name='send_tour_chat'),
    path('tour/<int:tour_id>/chat/', views.TourChatMessageList.as_view(), name='tour_chat_messages'),
]


