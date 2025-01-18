from base_serializers import UserBaseSerializer
from general.base_serializers import FileBaseSerializer, LocationBaseSerializer


class UserSerializer(UserBaseSerializer):
    pfp = FileBaseSerializer(read_only=True)
    location = LocationBaseSerializer(read_only=True)

    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + ('pfp', 'location',)
