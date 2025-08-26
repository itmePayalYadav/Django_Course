from . import validators
from .models import Product
from rest_framework import serializers
from rest_framework.reverse import reverse
from api.serializers import UserPublicSerializer

class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail",
        lookup_field="pk",
        read_only=True
    )
    title = serializers.CharField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    title = serializers.CharField(validators=[validators.validate_title, validators.validate_title_no_hello, validators.unique_product_title])
    body = serializers.CharField(source='content')

    class Meta:
        model = Product
        fields = [
            'id',
            'owner',
            'title',
            'body',
            'price',
            'sale_price',
            'public',
            'path',
            'endpoint'
        ]

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk":obj.id}, request=request)
