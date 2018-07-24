from rest_framework import generics, mixins, permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

# from django.shortcuts import get_object_or_404

from units.models import UnitReservation
from .serializers import UnitReservationSerializer


class UnitReservationAPIDetailView(
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.RetrieveAPIView
        ):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = UnitReservationSerializer
    queryset = UnitReservation.objects.all()
    loocup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UnitReservationListAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView
        ):

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = [SessionAuthentication]
    serializer_class = UnitReservationSerializer
    # passed_id = None

    def get_queryset(self):
        request = self.request
        qs = UnitReservation.objects.all()
        query = request.GET.get('q')
        # print('*-*-* query = ', query)
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
