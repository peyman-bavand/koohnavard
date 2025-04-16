# chat/factories.py

import factory
from factory.django import DjangoModelFactory
from chat.models import ChatGroup, ChatMessage, TourChatMessage
from group.models import Group
from tour.models import Tour
from django.contrib.auth import get_user_model

# فرض بر این است که این فکتوری‌ها از اپ‌های دیگر import می‌شوند:
from user.factories import CustomUserFactory
from group.factories import GroupFactory
from tour.factories import TourFactory

User = get_user_model()


class ChatGroupFactory(DjangoModelFactory):
    class Meta:
        model = ChatGroup

    group = factory.SubFactory(GroupFactory)


class ChatMessageFactory(DjangoModelFactory):
    class Meta:
        model = ChatMessage

    chat_group = factory.SubFactory(ChatGroupFactory)
    user = factory.SubFactory(CustomUserFactory )
    message = factory.Faker('sentence')
    is_read = factory.Faker('boolean')


class TourChatMessageFactory(DjangoModelFactory):
    class Meta:
        model = TourChatMessage

    tour = factory.SubFactory(TourFactory)
    sender = factory.SubFactory(CustomUserFactory )
    message = factory.Faker('paragraph')
