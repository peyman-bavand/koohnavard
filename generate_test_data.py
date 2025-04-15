# generate_test_data.py

import os
import django

# تنظیم محیط Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# import factories (تعداد بیشتر رو می‌تونی اضافه کنی)
from user.factories import CustomUserFactory, UserProfileFactory, NotificationSettingsFactory
from group.factories import GroupFactory, GroupMemberFactory, GroupImageGalleryFactory
from tour.factories import TourFactory, TourBookingFactory, TourReviewFactory, TourCategoryFactory
from payment.factories import PaymentFactory, PaymentItemFactory
from chat.factories import ChatGroupFactory, ChatMessageFactory, TourChatMessageFactory
from notification.factories import NotificationFactory

def generate():
    print("🔄 در حال ساخت داده‌های تستی...")

    # ساخت کاربران
    users = CustomUserFactory.create_batch(5)
    for user in users:
        UserProfileFactory(user=user)

    # ساخت گروه‌ها و اعضا
    groups = GroupFactory.create_batch(3)
    for group in groups:
        GroupMemberFactory(group=group, user=users[0])  # فقط یک عضو برای تست

    # ساخت تورها
    tours = TourFactory.create_batch(4)
    for tour in tours:
        TourBookingFactory(tour=tour, user=users[1])

    # پرداخت‌ها
    PaymentFactory.create_batch(2)
    PaymentItemFactory.create_batch(5)

    # چت و پیام‌ها
    chat_groups = ChatGroupFactory.create_batch(2)
    for chat_group in chat_groups:
        ChatMessageFactory.create_batch(3, chat_group=chat_group, sender=users[2])

    # اعلان‌ها
    NotificationFactory.create_batch(5)

    print("✅ داده‌های تستی با موفقیت ساخته شدند.")

if __name__ == "__main__":
    generate()
