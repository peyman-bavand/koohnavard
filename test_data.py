import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from user.factories import CustomUserFactory, UserProfileFactory, NotificationSettingsFactory
from group.factories import GroupFactory, GroupMemberFactory, GroupImageGalleryFactory
from tour.factories import TourFactory, TourBookingFactory, TourCategoryFactory, TourReviewFactory
from chat.factories import ChatGroupFactory, ChatMessageFactory, TourChatMessageFactory
from notification.factories import NotificationFactory
from payment.factories import PaymentFactory, PaymentItemFactory


def run():
    print("✅ ایجاد داده‌های تستی شروع شد...")

    users = [CustomUserFactory() for _ in range(10)]
    profiles = [UserProfileFactory(user=user) for user in users]
    notifications = [NotificationSettingsFactory(user=user) for user in users]

    groups = [GroupFactory(leader=users[i]) for i in range(3)]
    for group in groups:
        GroupMemberFactory(group=group, user=group.leader, role='Leader', status='Leader')
        for user in users:
            if user != group.leader:
                GroupMemberFactory(group=group, user=user)

    galleries = [GroupImageGalleryFactory(group=group) for group in groups]

    categories = [TourCategoryFactory() for _ in range(3)]
    tours = [TourFactory(leader=users[i % 10], group=groups[i % 3], category=categories[i % 3]) for i in range(5)]

    bookings = [TourBookingFactory(user=user, tour=tour) for user in users for tour in tours[:2]]
    reviews = [TourReviewFactory(user=user, tour=tour) for user in users[:5] for tour in tours[:3]]

    chat_groups = [ChatGroupFactory(group=group) for group in groups]
    chat_messages = [ChatMessageFactory(chat_group=chat_groups[i % 3], user=users[i % 10]) for i in range(20)]
    tour_messages = [TourChatMessageFactory(tour=tour, sender=users[i % 10]) for i, tour in enumerate(tours)]

    notifications = [NotificationFactory(user=user) for user in users]

    payments = [PaymentFactory(user=user) for user in users]
    payment_items = [PaymentItemFactory(payment=payments[i % len(users)], tour=tours[i % len(tours)]) for i in range(15)]

    print("🎉 داده‌های تستی با موفقیت ایجاد شدند.")


if __name__ == '__main__':
    run()
