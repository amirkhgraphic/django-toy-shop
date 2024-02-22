import uuid


def brand_path(instance, filename):
    return f'shop/brand/{uuid.uuid4().hex[:7]}.{filename.split(".")[-1]}'


def gallery_path(instance, filename):
    return f'shop/gallery/product_{instance.product_id}/{uuid.uuid4().hex[:7]}.{filename.split(".")[-1]}'


def product_path(instance, filename):
    return f'shop/product/user_{instance.seller_id}/{uuid.uuid4().hex[:7]}.{filename.split(".")[-1]}'
