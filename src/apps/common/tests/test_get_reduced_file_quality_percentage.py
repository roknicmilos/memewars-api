from apps.common.utils import get_reduced_file_quality_percentage
from meme_wars.tests.test_case import TestCase


class TestGetReducedFileQualityPercentage(TestCase):
    def test_should_return_correct_reduced_image_quality_percentage(self):
        self.assertEqual(get_reduced_file_quality_percentage(file_size=50000), 100)
        self.assertEqual(get_reduced_file_quality_percentage(file_size=99999), 100)

        self.assertEqual(get_reduced_file_quality_percentage(file_size=100000), 80)
        self.assertEqual(get_reduced_file_quality_percentage(file_size=299999), 80)

        self.assertEqual(get_reduced_file_quality_percentage(file_size=300000), 70)
        self.assertEqual(get_reduced_file_quality_percentage(file_size=599999), 70)

        self.assertEqual(get_reduced_file_quality_percentage(file_size=600000), 60)
        self.assertEqual(get_reduced_file_quality_percentage(file_size=999999), 60)

        self.assertEqual(get_reduced_file_quality_percentage(file_size=1000000), 50)
        self.assertEqual(get_reduced_file_quality_percentage(file_size=1500000), 50)
        self.assertEqual(get_reduced_file_quality_percentage(file_size=10000000), 50)
