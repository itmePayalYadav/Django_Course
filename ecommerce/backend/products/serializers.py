from rest_framework import serializers
from rest_framework.reverse import reverse
from api.serializers import UserPublicSerializer
from .models import Product
from . import validators

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='pk')
    title = serializers.CharField(validators=[validators.validate_title, validators.validate_title_no_hello, validators.unique_product_title])
    # name = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'owner',
            'title',
            # 'name',
            'content',
            'price',
            'sale_price',
            'my_discount',
            'url',
            'edit_url'
        ]

    # def create(self, validated_data):
    #     obj = super().create(validated_data)
    #     return obj

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title')
    #     return instance

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk":obj.id}, request=request)

    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None

        if not isinstance(obj, Product):
            return None

        return obj.get_discount()
