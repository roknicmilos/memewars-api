from unittest.mock import patch

from apps.wars.models import War
from apps.wars.models import meme as meme_model_file
from apps.wars.tests.factories import MemeFactory, VoteFactory, WarFactory
from meme_wars.tests.test_case import TestCase


class TestMeme(TestCase):
    def test_should_raise_validation_error_when_war_is_not_in_submission_phase(self):
        war = WarFactory()
        self.assertNotEqual(war.phase, War.Phases.SUBMISSION)
        meme = MemeFactory(war=war)
        expected_validation_errors = {
            "war": [f'War must be in "{War.Phases.SUBMISSION.label}" phase'],
        }
        with self.raisesDjangoValidationError(match=expected_validation_errors):
            meme.full_clean()

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

    @patch.object(meme_model_file, "compress_image_file")
    def test_should_compress_image_when_meme_is_created(self, mock_compress_image_file):
        mock_compress_image_file.return_value = None
        MemeFactory(image="fixtures/memes/meme_template_1.jpg")
        mock_compress_image_file.assert_called_once()

    @patch.object(meme_model_file, "compress_image_file")
    def test_should_not_compress_image_when_meme_image_is_not_update(self, mock_compress_image_file):
        mock_compress_image_file.return_value = None
        meme = MemeFactory(image="fixtures/memes/meme_template_1.jpg")
        mock_compress_image_file.assert_called_once()

        mock_compress_image_file.reset_mock()

        meme.update(is_approved=True)
        mock_compress_image_file.assert_not_called()

    @patch.object(meme_model_file, "compress_image_file")
    def test_should_compress_image_when_meme_image_is_update(self, mock_compress_image_file):
        mock_compress_image_file.return_value = None
        meme = MemeFactory(image="fixtures/memes/meme_template_1.jpg")
        mock_compress_image_file.assert_called_once()

        mock_compress_image_file.reset_mock()

        meme.update(image="fixtures/memes/meme_template_2.jpg")
        mock_compress_image_file.assert_called_once()

    def test_should_raise_validation_error_when_meme_upload_limit_is_exceeded(self):
        war = WarFactory(meme_upload_limit=1)
        meme = MemeFactory(war=war)  # user has reached meme upload limit
        MemeFactory(war=war)  # another user has reached meme upload limit

        expected_error_message = "This user already reached Meme upload limit in this war."
        with self.raisesDjangoValidationError(match=expected_error_message, code="meme_upload_limit_reached"):
            MemeFactory(war=war, user=meme.user)
