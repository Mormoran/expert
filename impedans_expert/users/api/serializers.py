from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
)

from impedans_expert.users.models import User

##############################################################################
# Define API serializers for User related operations create, detail and list #
##############################################################################

class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name'
        ]

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name'
        ]

class UserListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='users_api:user_list_detail',
        lookup_field='pk'
    )
    delete_url = HyperlinkedIdentityField(
        view_name='users_api:user_list_delete',
        lookup_field='pk'
    )
    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'name',
            'delete_url'
        ]