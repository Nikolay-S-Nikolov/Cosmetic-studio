from django.test import TestCase
from django.contrib.auth import get_user_model
from Cosmetic_studio.common.models import TeamMemberCard

UserModel = get_user_model()


class TeamMemberCardModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(email='testuser@example.com', password='testpass123')

    def test__create_team_member_card__with_only_created_by(self):
        team_member_card = TeamMemberCard.objects.create(created_by=self.user)
        self.assertIsNotNone(team_member_card)
        self.assertEqual(team_member_card.created_by, self.user)
        self.assertIsNone(team_member_card.name)
        self.assertIsNone(team_member_card.title)
        self.assertIsNone(team_member_card.description)
        self.assertIsNone(team_member_card.role)
        self.assertIsNone(team_member_card.specialities)
        self.assertTrue(team_member_card.is_active)
        self.assertEqual(team_member_card.appearance_order, 2)

    def test__str__returns_name(self):
        team_member_card = TeamMemberCard.objects.create(
            created_by=self.user,
            name="Arnold Schwarzenegger"
        )
        self.assertEqual(str(team_member_card), "Arnold Schwarzenegger")

    def test__team_member_card__default_ordering(self):
        card1 = TeamMemberCard.objects.create(
            name='Member 1',
            appearance_order=1,
            created_by=self.user
        )
        card2 = TeamMemberCard.objects.create(
            name='Member 2',
            appearance_order=2,
            created_by=self.user
        )
        card3 = TeamMemberCard.objects.create(
            name='Member 3',
            appearance_order=1,
            created_by=self.user
        )

        cards = TeamMemberCard.objects.all()
        self.assertEqual(list(card.name for card in cards), ['Member 3', 'Member 1', 'Member 2'])
