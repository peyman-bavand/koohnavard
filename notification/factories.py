import factory
from .models import Notification
from user.factories import CustomUserFactory
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
