from apps.wars.models import Vote
from apps.wars.serializers import VoteSerializer


class PatchVoteSerializer(VoteSerializer):
    class Meta:
        model = Vote
        fields = "__all__"
        read_only_fields = ["user", "meme", "submission_count"]

    def create(self, validated_data: dict) -> None:
        pass  # pragma: no cover

    def update(self, instance: Vote, validated_data: dict) -> Vote:
        validated_data["submission_count"] = instance.submission_count + 1
        return super().update(instance=instance, validated_data=validated_data)
