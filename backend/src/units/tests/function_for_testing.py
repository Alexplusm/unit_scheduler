from django.contrib.auth.models import User

from ..models import (
    Unit,
    UnitUserProfile,
    UnitReservation
    )


def create_user(**kwargs):
    """
        - username
        - first_name
        - last_name
        - email
    """
    return User.objects.create_user(**kwargs)


def create_profile(**kwargs):
    """
        user = OneToOneField - User
        tester = BooleanField - (default=True)
        boss = BooleanField - (default=False)
        superboss = BooleanField - (default=False)
        notice_me = BooleanField - (default=False)
        note_text = TextField - (blank=True, null=True)
         - - - -
        # ntg = ForeignKey - NTGroup
    """
    return UnitUserProfile.objects.create(**kwargs)


def create_unit(**kwargs):
    """
        unit_name = CharField - (unique=True, max_length=100)
        unit_manager = ForeignKey - (User)
        unit_notice_users = ManyToManyField - (User, blank=True)
        note_text = TextField - (blank=True, null=True)
        # режим работы
        parallel_records = BooleanField - (default=False)
        start_work = TimeField - (default=time(9, 0))
        end_work = TimeField - (default=time(21, 0))
        # длительность записи в днях
        duration_of_record = DurationField - (default=timedelta_dt(days=1))
    """
    return Unit.objects.create(**kwargs)


def create_reservation(**kwargs):
    """
        unit = ForeignKey - (Unit)
        start_work = DateTimeField
        end_work = DateTimeField
        tester = ForeignKey - (User)
        # contract = ForeignKey - (Contract)
        test_object = CharField - (max_length=20)
            DISTANCE_CHOICES = (
                (1, u'малое'),
                (2, u'среднее'),
                (3, u'большое'),
                )
        distance = IntegerField -
            (choices=DISTANCE_CHOICES, blank=False, null=True, default=2)
        note_text = models.TextField - (blank=True, null=True)
        reg_date = models.DateTimeField - (auto_now_add=True, auto_now=False)
        edit_date = models.DateTimeField - (auto_now_add=False, auto_now=True)
        owner = models.ForeignKey - ('auth.User')
    """
    return UnitReservation.objects.create(**kwargs)