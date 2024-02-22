from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


from apis.shop.serializers import LikeCreateSerializer, CategoryCreateSerializer, GallerySerializer
from apps.shop.models import Like, Category, CategoryProduct, Gallery


@api_view(['POST'])
def like_api_view(request, product_id, user_id):
    try:
        like = Like.objects.get(product_id=product_id, user_id=user_id)
        like.delete()
        return Response({'detail': 'removed'}, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        like_data = {'product': product_id, 'user': user_id}
        serializer = LikeCreateSerializer(data=like_data)
        if serializer.is_valid():
            Like.objects.create(product_id=product_id, user_id=user_id)
            return Response({'detail': 'created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryCreateAPIView(CreateAPIView):
    model = Category
    serializer_class = CategoryCreateSerializer

    def create(self, request, *args, **kwargs):
        category_name = request.data.get('name')
        existing_category = Category.objects.filter(name__iexact=category_name).first()

        if existing_category:
            serializer = self.get_serializer(existing_category)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryProductDeleteAPIView(APIView):
    def delete(self, request):
        product_id = request.query_params.get('product_id')
        category_id = request.query_params.get('category_id')

        if product_id is None or category_id is None:
            return Response({'error': 'product_id and category_id are required in query parameters'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            category_product = CategoryProduct.objects.get(product_id=product_id, category_id=category_id)
            category_product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CategoryProduct.DoesNotExist:
            return Response({'error': 'CategoryProduct does not exist'}, status=status.HTTP_404_NOT_FOUND)


class GalleryCreateAPIView(CreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        serializer.save(product_id=product_id)


class GalleryDeleteAPIView(DestroyAPIView):
    queryset = Gallery.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
