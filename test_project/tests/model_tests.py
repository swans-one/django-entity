from django.contrib.contenttypes.models import ContentType
from entity.models import Entity

from test_project.models import Account, Team
from .utils import EntityTestCase


class TestEntityModel(EntityTestCase):
    """
    Tests custom functionality in the Entity model.
    """
    def test_get_super_entities_none(self):
        """
        Tests that super entities are retrieved for mirroed entities that
        have no super entities
        """
        # Create an account with no team
        account = Account.objects.create()
        # Get its resulting entity
        entity = Entity.objects.get(entity_type=ContentType.objects.get_for_model(account), entity_id=account.id)
        # Get its super entities. It should be an empty list
        self.assertEquals(entity.get_super_entities(), [])

    def test_get_super_entities_one(self):
        """
        Tests retrieval of super entities when an entity has exactly one.
        """
        # Create a team and an account with the team as a super entity.
        team = Team.objects.create()
        account = Account.objects.create(team=team)
        # Get the entity of the account and the team
        account_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(account), entity_id=account.id)
        team_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(team), entity_id=team.id)
        # Verify that the super entities of the account is the team
        self.assertEquals(account_entity.get_super_entities(), [team_entity])

    def test_get_sub_entities_none(self):
        """
        Tests retrieval of sub entities when an entity has none.
        """
        # Create a team
        team = Team.objects.create()
        # Get the entity of the team
        team_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(team), entity_id=team.id)
        # Verify that the sub entities of the team is an empty list
        self.assertEquals(team_entity.get_super_entities(), [])

    def test_get_sub_entities_one(self):
        """
        Tests retrieval of sub entities when an entity has exactly one.
        """
        # Create a team and an account with the team as a super entity.
        team = Team.objects.create()
        account = Account.objects.create(team=team)
        # Get the entity of the account and the team
        account_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(account), entity_id=account.id)
        team_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(team), entity_id=team.id)
        # Verify that the sub entities of the team is the account
        self.assertEquals(team_entity.get_sub_entities(), [account_entity])

    def test_get_active_sub_entities_relationships_one(self):
        """
        Tests retrieval of all active sub entities when one exists.
        """
        # Create a team and an account with the team as a super entity.
        team = Team.objects.create()
        account = Account.objects.create(team=team)
        # Get the entity of the account and the team
        account_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(account), entity_id=account.id)
        team_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(team), entity_id=team.id)
        # Verify that the active sub entities of the team is the account
        self.assertEquals(team_entity.get_sub_entities(is_active=True), [account_entity])
        # Verify that the inactive sub entities of the team is nothing
        self.assertEquals(team_entity.get_sub_entities(is_active=False), [])

    def test_get_inactive_sub_entities_relationships_one(self):
        """
        Tests retrieval of all inactive sub entities when one exists.
        """
        # Create a team and an account with the team as a super entity. The
        # account is the captain, so according to our test app definition, it has
        # an inactive relationship with the team
        team = Team.objects.create()
        account = Account.objects.create(team=team, is_captain=True)
        # Get the entity of the account and the team
        account_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(account), entity_id=account.id)
        team_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(team), entity_id=team.id)
        # Verify that the inactive sub entities of the team is the account
        self.assertEquals(team_entity.get_sub_entities(is_active=False), [account_entity])
        # Verify that the active sub entities of the team is none
        self.assertEquals(team_entity.get_sub_entities(is_active=True), [])

    def test_get_inactive_sub_entities_one(self):
        """
        Tests retrieval of all inactive sub entities when one exists. This test tests
        when the relationship is active but the entity itself is inactive. In this case
        the inactiveness of the entity should override the activeness of the relationship.
        """
        # Create a team and an account with the team as a super entity. Make the relationship
        # active but the entity inactive
        team = Team.objects.create()
        account = Account.objects.create(team=team, is_active=False)
        # Get the entity of the account and the team
        account_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(account), entity_id=account.id)
        team_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(team), entity_id=team.id)
        # Verify that the active sub entities of the team is nothing
        self.assertEquals(team_entity.get_sub_entities(is_active=True), [])
        # Verify that the inactive sub entities of the team is the account
        self.assertEquals(team_entity.get_sub_entities(is_active=False), [account_entity])

    def test_get_active_super_entities_relationships_one(self):
        """
        Tests retrieval of all active super entities when one exists.
        """
        # Create a team and an account with the team as a super entity.
        team = Team.objects.create()
        account = Account.objects.create(team=team)
        # Get the entity of the account and the team
        account_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(account), entity_id=account.id)
        team_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(team), entity_id=team.id)
        # Verify that the active super entities of the account is the team
        self.assertEquals(account_entity.get_super_entities(is_active=True), [team_entity])
        # Verify that the inactive super entities of the account is nothing
        self.assertEquals(account_entity.get_super_entities(is_active=False), [])

    def test_get_inactive_super_entities_relationships_one(self):
        """
        Tests retrieval of all inactive super entities when one exists.
        """
        # Create a team and an account with the team as a super entity. The
        # account is the captain, so according to our test app definition, it has
        # an inactive relationship with the team
        team = Team.objects.create()
        account = Account.objects.create(team=team, is_captain=True)
        # Get the entity of the account and the team
        account_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(account), entity_id=account.id)
        team_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(team), entity_id=team.id)
        # Verify that the inactive super entities of the account is the team
        self.assertEquals(account_entity.get_super_entities(is_active=False), [team_entity])
        # Verify that the active super entities of the account is none
        self.assertEquals(account_entity.get_super_entities(is_active=True), [])

    def test_get_inactive_super_entities_one(self):
        """
        Tests retrieval of all inactive super entities when one exists. This test tests
        when the relationship is active but the entity itself is inactive. In this case
        the inactiveness of the entity should override the activeness of the relationship.
        """
        # Create a team and an account with the team as a super entity. Make the relationship
        # active but the entity inactive
        team = Team.objects.create(is_active=False)
        account = Account.objects.create(team=team)
        # Get the entity of the account and the team
        account_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(account), entity_id=account.id)
        team_entity = Entity.objects.get(
            entity_type=ContentType.objects.get_for_model(team), entity_id=team.id)
        # Verify that the active super entities of the team is nothing
        self.assertEquals(account_entity.get_sub_entities(is_active=True), [])
        # Verify that the inactive suoer entities of the account is the team
        self.assertEquals(account_entity.get_super_entities(is_active=False), [team_entity])
