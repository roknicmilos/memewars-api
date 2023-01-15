from unittest.mock import patch
from apps.common.tests import TestCase
from apps.users.tests.factories import UserFactory
from apps.wars.models import Meme, War
from apps.wars.tests.factories import WarFactory, VoteFactory, MemeFactory


class TestMeme(TestCase):

    def test_should_raise_validation_error_when_war_is_not_in_submission_phase(self):
        user = UserFactory()
        war = WarFactory()
        self.assertNotEqual(war.phase, War.Phases.SUBMISSION)
        meme = Meme(war=war, user=user)
        self.assertValidationError(
            obj=meme,
            expected_message=f'War must be in "{War.Phases.SUBMISSION.label}" phase',
            expected_code='limit_war_phase',
            field_name='war'
        )

    def test_should_return_correct_total_score(self):
        meme = MemeFactory()
        self.assertFalse(meme.votes.exists())
        self.assertEqual(meme.total_score, 0)

        VoteFactory(meme=meme, score=10)
        self.assertEqual(meme.total_score, 10)

        VoteFactory(meme=meme, score=5)
        self.assertEqual(meme.total_score, 7.5)

        VoteFactory(meme=meme, score=7)
        self.assertEqual(meme.total_score, 7.33)

    def test_should_return_correct_vote_count(self):
        meme = MemeFactory()
        self.assertEqual(meme.votes.count(), 0)

        VoteFactory(meme=meme)
        self.assertEqual(meme.votes.count(), 1)

        VoteFactory()
        self.assertEqual(meme.votes.count(), 1)

        VoteFactory(meme=meme)
        self.assertEqual(meme.votes.count(), 2)

    @patch('apps.wars.models.meme.compress_image_file')
    def test_should_compress_image_when_meme_is_created(self, mock_compress_image_file):
        mock_compress_image_file.return_value = None
        MemeFactory(image='fixtures/meme_template_1.jpg')
        mock_compress_image_file.assert_called_once()

    @patch('apps.wars.models.meme.compress_image_file')
    def test_should_not_compress_image_when_meme_image_is_not_update(self, mock_compress_image_file):
        mock_compress_image_file.return_value = None
        meme = MemeFactory(image='fixtures/meme_template_1.jpg')
        mock_compress_image_file.assert_called_once()

        mock_compress_image_file.reset_mock()

        meme.update(is_approved=True)
        mock_compress_image_file.assert_not_called()

    @patch('apps.wars.models.meme.compress_image_file')
    def test_should_compress_image_when_meme_image_is_update(self, mock_compress_image_file):
        mock_compress_image_file.return_value = None
        meme = MemeFactory(image='fixtures/meme_template_1.jpg')
        mock_compress_image_file.assert_called_once()

        mock_compress_image_file.reset_mock()

        meme.update(image='fixtures/meme_template_2.jpg')
        mock_compress_image_file.assert_called_once()
