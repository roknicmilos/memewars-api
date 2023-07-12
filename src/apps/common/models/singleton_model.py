from apps.common.models import BaseModel


class SingletonModel(BaseModel):
    class Meta:
        abstract = True

    def save(self, **kwargs) -> None:
        self.pk = 1
        super().save(**kwargs)

    def delete(self, *args, **kwargs) -> None:
        pass

    @classmethod
    def load(cls) -> "SingletonModel":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @classmethod
    def exists(cls) -> bool:
        return cls.objects.exists()

    @classmethod
    def update(cls, **kwargs) -> None:
        instance = cls.load()
        super().update(self=instance, **kwargs)
