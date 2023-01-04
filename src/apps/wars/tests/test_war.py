from apps.common.tests import TestCase
from apps.wars.models import War


class TestWar(TestCase):

    def test_war_should_have_expected_default_values(self):
        war = War.objects.create(name='Meme war')
        self.assertEqual(war.phase, War.Phases.PREPARATION)
        self.assertFalse(war.requires_meme_approval)
