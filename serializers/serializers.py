from marshmallow import Serializer, fields


class SerializeUserData(Serializer):
    class Meta:
        fields = ("id", "email", "password")
