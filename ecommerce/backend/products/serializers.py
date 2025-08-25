from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='pk')

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount',
            'url',
            'edit_url'
        ]

    def validate_title(self, value):
        qs = Product.objects.filter(title__exact=value)
        if qs.exists():
            raise serializers.validationError(f"This {value} is already a product name.")
        return value

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
