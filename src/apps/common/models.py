from django_extensions.db.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    class Meta:
        abstract = True

    def update(self, **kwargs):
        for field_name, field_value in kwargs.items():
            setattr(self, field_name, field_value)
        self.save()
