from django.db import models

from apps.common.models.singleton_model import SingletonModel
from meme_wars.tests.test_case import TestCase


class TestSingletonModel(TestCase):
    class ConcreteSingletonModel(SingletonModel):
        """
        This model will be migrated to the temporary tests
        database(s) even though it has no migration files.
        Model migration will FAIL if the app has migrations
        (module "migrations").
        """

        name = models.CharField(max_length=100, default="")

        class Meta:
            app_label = "common"

    def test_should_override_pk_before_saving_instance(self):
        singleton_instance = self.ConcreteSingletonModel(pk=10)
        self.assertEqual(singleton_instance.pk, 10)
        singleton_instance.save()
        self.assertEqual(singleton_instance.pk, 1)

    def test_should_not_delete_instance(self):
        singleton_instance = self.ConcreteSingletonModel.objects.create()
        singleton_instance.delete()
        singleton_instance.refresh_from_db()
        self.assertIsNotNone(singleton_instance)

    def test_should_load_instance_by_creating_it_first(self):
        self.assertFalse(self.ConcreteSingletonModel.objects.exists())
        singleton_instance = self.ConcreteSingletonModel.load()
        self.assertIsInstance(singleton_instance, self.ConcreteSingletonModel)

    def test_should_load_instance_by_fetching_existing_one(self):
        singleton_instance = self.ConcreteSingletonModel.objects.create()
        self.assertEqual(self.ConcreteSingletonModel.objects.count(), 1)
        self.assertEqual(self.ConcreteSingletonModel.load(), singleton_instance)
        self.assertEqual(self.ConcreteSingletonModel.objects.count(), 1)

    def test_should_return_true_when_instance_exists_and_false_when_it_does_not_exist(self):
        self.assertFalse(self.ConcreteSingletonModel.exists())
        self.ConcreteSingletonModel.load()
        self.assertTrue(self.ConcreteSingletonModel.exists())

    def test_should_update_instance_using_class_method(self):
        instance = self.ConcreteSingletonModel.load()
        self.assertEqual(instance.name, "")
        self.ConcreteSingletonModel.update(name="Miki")
        instance.refresh_from_db()
        self.assertEqual(instance.name, "Miki")
