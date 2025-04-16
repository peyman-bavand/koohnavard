from django.core.management.base import BaseCommand
from user.factories import CustomUserFactory, UserProfileFactory, NotificationSettingsFactory
from group.factories import GroupFactory, GroupMemberFactory, GroupImageGalleryFactory
from tour.factories import TourCategoryFactory, TourFactory, TourBookingFactory, TourReviewFactory
from chat.factories import ChatGroupFactory, ChatMessageFactory, TourChatMessageFactory
from notification.factories import NotificationFactory
from payment.factories import PaymentFactory, PaymentItemFactory

class Command(BaseCommand):
    help = 'Seed the database with fake data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding data...'))

        users = CustomUserFactory.create_batch(10)
        for user in users:
            UserProfileFactory(user=user)
            NotificationSettingsFactory(user=user)
            NotificationFactory(user=user)

        groups = GroupFactory.create_batch(5)
        for group in groups:
            GroupMemberFactory(group=group)
            GroupImageGalleryFactory(group=group)

        categories = TourCategoryFactory.create_batch(3)
        for group in groups:
            for _ in range(2):
                tour = TourFactory(group=group, category=categories[0])
                TourBookingFactory(tour=tour)
                TourReviewFactory(tour=tour)
                TourChatMessageFactory(tour=tour)

        chat_groups = ChatGroupFactory.create_batch(5)
        for cg in chat_groups:
            ChatMessageFactory(chat_group=cg)

        for _ in range(5):
            payment = PaymentFactory()
            PaymentItemFactory(payment=payment)

        self.stdout.write(self.style.SUCCESS('Data seeded successfully.'))
