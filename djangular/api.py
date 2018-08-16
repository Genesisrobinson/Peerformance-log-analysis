from rest_framework.generics import ListAPIView

from .serializers import listserializer,cardserializer
from .models import List,card

class ListAPI(ListAPIView):
    queryset =List.objects.all()
    serializer_class=listserializer

class cardAPI(ListAPIView):
    queryset =card.objects.all()
    serializer_class=cardserializer

