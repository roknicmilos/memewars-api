from django_extensions.db.models import TimeStampedModel
from apps.common.models import OriginalModelInstance


class BaseModel(TimeStampedModel):
    class Meta:
        abstract = True

    verbose_name: str = None
    verbose_name_plural: str = None

    def __new__(cls, *args, **kwargs):
        cls.verbose_name = cls._meta.verbose_name
        cls.verbose_name_plural = cls._meta.verbose_name_plural
        return super(BaseModel, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)
        self._original = None

    def refresh_from_db(self, using=None, fields=None):
        super(BaseModel, self).refresh_from_db()
        self._original = None

    @property
    def original(self) -> OriginalModelInstance | None:
        if not self._original and self.pk:
            self._original = OriginalModelInstance(model_claas=self.__class__, obj_id=self.pk)
        return self._original

    def update(self, **kwargs):
        for field_name, field_value in kwargs.items():
            setattr(self, field_name, field_value)
        self.save()
