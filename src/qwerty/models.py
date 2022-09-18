from django_extensions.db.models import TimeStampedModel


# TODO: move to "core" app
class BaseModel(TimeStampedModel):
    class Meta:
        abstract = True
