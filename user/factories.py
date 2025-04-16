import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.contrib.auth.models import Group, Permission
from user.models import CustomUser, UserProfile, NotificationSettings

faker = Faker('fa_IR')


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda _: faker.email())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    date_of_birth = factory.LazyAttribute(lambda _: faker.date_of_birth(minimum_age=18, maximum_age=60))
    phone_number = factory.LazyAttribute(lambda _: faker.phone_number())
    profile_picture = None  # اگر بخوای میشه فیک ایمیج جنریت کرد
    gender = factory.LazyAttribute(lambda _: faker.random_element(elements=['Male', 'Female']))
    date_joined = factory.LazyFunction(faker.date_time_this_decade)
    is_active = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.groups.add(group)

    @factory.post_generation
    def user_permissions(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for perm in extracted:
                self.user_permissions.add(perm)


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(CustomUserFactory)
    bio = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=200))
    address = factory.LazyAttribute(lambda _: faker.address())
    # created_at و updated_at توسط auto_now و auto_now_add ساخته می‌شن


class NotificationSettingsFactory(DjangoModelFactory):
    class Meta:
        model = NotificationSettings

    user = factory.SubFactory(CustomUserFactory)
    email_notifications = factory.LazyAttribute(lambda _: faker.boolean(chance_of_getting_true=80))
    push_notifications = factory.LazyAttribute(lambda _: faker.boolean(chance_of_getting_true=70))
    sms_notifications = factory.LazyAttribute(lambda _: faker.boolean(chance_of_getting_true=30))
