import uuid


def gallery_path(instance, filename):
    return f'blog/gallery/post_{instance.post_id}/{uuid.uuid4().hex[:7]}.{filename.split(".")[-1]}'


def post_path(instance, filename):
    return f'blog/post/user_{instance.author_id}/{uuid.uuid4().hex[:7]}.{filename.split(".")[-1]}'
