from rest_framework import serializers
from units.models import UnitReservation


class UnitReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitReservation
        fields = (
            'unit',
            'start_work',
            'end_work',
            'tester',
            'distance',
            # 'contract',
            'test_object',
            'note_text',
            'reg_date',
            'edit_date',
            'owner',
            'id'
        )

        read_only_fields = ['owner']

    # def validation_<field>(self, value):

    def validate(self, data):
        return data
