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




from django.utils import timezone
from group.models import Group, GroupMember, GroupImageGallery


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




# tour/factories.py

from factory.django import DjangoModelFactory
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

from group.factories import GroupFactory  # فرض بر اینکه GroupFactory رو ساختی
from tour.models import TourCategory, Tour, TourBooking, TourReview

User = get_user_model()

class TourCategoryFactory(DjangoModelFactory):
    class Meta:
        model = TourCategory

    name = factory.Faker('word')
    description = factory.Faker('text')


class TourFactory(DjangoModelFactory):
    class Meta:
        model = Tour

    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('paragraph')
    leader = factory.SubFactory('user.factories.CustomUserFactory ')  # اگه CustomUserFactory  جای دیگه ساختی
    start_date = factory.LazyFunction(lambda: timezone.now().date())
    end_date = factory.LazyFunction(lambda: (timezone.now() + timedelta(days=5)).date())
    price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    category = factory.SubFactory(TourCategoryFactory)
    location = factory.Faker('city')
    group = factory.SubFactory(GroupFactory)


class TourBookingFactory(DjangoModelFactory):
    class Meta:
        model = TourBooking

    user = factory.SubFactory('user.factories.CustomUserFactory ')
    tour = factory.SubFactory(TourFactory)
    booking_date = factory.LazyFunction(timezone.now)


class TourReviewFactory(DjangoModelFactory):
    class Meta:
        model = TourReview

    tour = factory.SubFactory(TourFactory)
    user = factory.SubFactory('user.factories.CustomUserFactory ')
    rating = factory.Iterator([1, 2, 3, 4, 5])
    comment = factory.Faker('paragraph')
    created_at = factory.LazyFunction(timezone.now)



# chat/factories.py

from chat.models import ChatGroup, ChatMessage, TourChatMessage
from group.models import Group
from tour.models import Tour

# فرض بر این است که این فکتوری‌ها از اپ‌های دیگر import می‌شوند:
from user.factories import CustomUserFactory 
from group.factories import GroupFactory
from tour.factories import TourFactory


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




from notification.models import Notification

# استفاده از کاربر موجود
class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification
    
    # فرض بر این است که user از قبل در سیستم وجود دارد
    user = factory.SubFactory(CustomUserFactory)  # استفاده از کاربر موجود
    title = factory.Faker('sentence', nb_words=6)  # عنوان تصادفی
    message = factory.Faker('text')  # پیام تصادفی
    created_at = factory.Faker('date_this_year')  # تاریخ تصادفی در سال جاری
    is_read = factory.Faker('boolean')  # وضعیت خواندن به صورت تصادفی

 



from django.utils import timezone
from payment.models import Payment, PaymentItem
from user.factories import CustomUser  # فرض می‌کنیم Factory مربوط به User در این مسیر قرار دارد.
from tour.factories import TourFactory  # فرض می‌کنیم Factory مربوط به Tour در این مسیر قرار دارد.

class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory(CustomUser)  # استفاده از SubFactory برای ایجاد یک کاربر به صورت خودکار
    amount = factory.Faker('random_number', digits=5)
    authority = factory.Faker('word')
    is_paid = factory.Faker('boolean')
    payment_date = factory.LazyFunction(timezone.now)  # زمان پرداخت را به صورت خودکار تنظیم می‌کند

class PaymentItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentItem

    payment = factory.SubFactory(PaymentFactory)  # ایجاد یک Payment به صورت خودکار
    tour = factory.SubFactory(TourFactory)  # ایجاد یک Tour به صورت خودکار
    amount = factory.Faker('random_number', digits=5)
