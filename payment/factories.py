import factory
from django.utils import timezone
from .models import Payment, PaymentItem
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
