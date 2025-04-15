import factory
from django.utils import timezone
from faker import Faker
from user.models import CustomUser
from .models import Group, GroupMember, GroupImageGallery

fake = Faker()

class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Faker('word')
    description = factory.Faker('paragraph')
    leader = factory.SubFactory('user.factories.CustomUserFactory')  # استفاده از factory مربوط به CustomUser
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

class GroupMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GroupMember

    group = factory.SubFactory(GroupFactory)
    user = factory.SubFactory('user.factories.CustomUserFactory')  # استفاده از factory مربوط به CustomUser
    joined_at = factory.LazyFunction(timezone.now)
    status = factory.Iterator(['Member', 'Leader', 'Left'])
    role = factory.Iterator(['Member', 'Leader', 'Manager'])

class GroupImageGalleryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GroupImageGallery

    group = factory.SubFactory(GroupFactory)
    image = factory.django.ImageField()
    caption = factory.Faker('sentence')
    uploaded_at = factory.LazyFunction(timezone.now)
