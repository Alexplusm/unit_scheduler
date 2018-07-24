import datetime

from django.test import TestCase
from ..models import (
    Unit,
    # UnitUserProfile,
    # UnitReservation
    )
from .function_for_testing import (
    create_user,
    create_profile,
    create_unit,
    create_reservation,
    )

"""
    todo:
    # переименовать модель UnitSchedule ????

"""


class UnitUserProfileModelTestCase(TestCase):

    def setUp(self):
        self.user = create_user(
                                username='AlexTester47',
                                first_name='alex',
                                last_name='green'
                                )

    def test_profile(self):
        profile = create_profile(user=self.user)
        self.assertEqual(str(profile), 'green a.')
    
    def test_profile_get_fio(self):
        profile = create_profile(user=self.user)
        self.assertEqual(profile.get_fio(), 'green a.')
        
    def test_profile_tester_1(self):
        profile = create_profile(user=self.user, tester=True)
        self.assertEqual(profile.tester, True)
    
    def test_profile_tester_2(self):
        profile = create_profile(user=self.user, tester=True)
        self.assertEqual(profile.boss, False)

    def test_profile_tester_3(self):
        profile = create_profile(user=self.user, tester=True)
        self.assertEqual(profile.superboss, False)

    def test_profile_tester_4(self):
        profile = create_profile(
                                user=self.user,
                                tester=True,
                                note_text='some note'
                                )
        self.assertEqual(profile.note_text, 'some note')
    
    def test_profile_tester_5(self):
        profile = create_profile(user=self.user, tester=True)
        self.assertEqual(profile.notice_me, False)

    def test_profile_tester_6(self):
        profile = create_profile(
                                user=self.user,
                                tester=True,
                                notice_me=True
                                )
        self.assertEqual(profile.notice_me, True)

    def test_profile_tester_7(self):
        profile = create_profile(
                                user=self.user,
                                tester=True,
                                notice_me=True,
                                note_text='note'
                                )
        self.assertEqual(profile.notice_me, True)
        self.assertEqual(profile.note_text, 'note')


class UnitModelTestCase(TestCase):
    """
        unit_name = models.CharField - 
            (verbose_name='Наименование', unique=True, max_length=100)
        unit_manager = models.ForeignKey(
            User, verbose_name='Начальник установки')
        unit_notice_users = models.ManyToManyField(
            User, related_name='unit_notice',
            verbose_name='Уведомления', blank=True)
        note_text = models.TextField('Примечания', blank=True, null=True)

        # режим работы
        parallel_records = models.BooleanField(default=False)
        # временной режим работы
        start_work = models.TimeField(
        verbose_name='Время начала работы установки', default=time(9, 0))
        end_work = models.TimeField(
        verbose_name='Время окончания работы установки', default=time(21, 0))
        # длительность записи в днях
        duration_of_record = models.DurationField(
        verbose_name='Длительность записи', default=timedelta_dt(days=1))
    """

    def setUp(self):
        self.user = create_user(
                                username='AlexTester47',
                                first_name='alex',
                                last_name='green'
                                )

    def test_unit_create_unit_with_default_user(self):
        profile = create_profile(user=self.user)
        unit = create_unit(unit_manager=profile)
        self.assertTrue(isinstance(unit, Unit))


class UnitReservationTestCase(TestCase):

    """
        unit = models.ForeignKey(Unit, verbose_name="Установка")
        start_work = models.DateTimeField("Дата и время начала работы")
        end_work = models.DateTimeField("Дата и время окончания работы")
        tester = models.ForeignKey(User, verbose_name="Испытатель")
        # contract = models.ForeignKey(Contract, verbose_name="Договор", on_delete=models.PROTECT)
        test_object = models.CharField("Объект испытаний", max_length=20)
        DISTANCE_CHOICES = (
            (1, u'малое'),
            (2, u'среднее'),
            (3, u'большое'),
            )
        distance = models.IntegerField(
            "Расстояние", choices=DISTANCE_CHOICES, blank=False, null=True, default=2)
        note_text = models.TextField(
            'Примечания', help_text=u"Укажите режим и требуемые уровни", blank=True, null=True)
        reg_date = models.DateTimeField(
            'Дата регистрации', auto_now_add=True, auto_now=False)
        edit_date = models.DateTimeField(
            'Дата изменений', auto_now_add=False, auto_now=True)
        owner = models.ForeignKey(
            'auth.User', related_name='unit_schedule', on_delete=models.CASCADE)
    """

    def create_unit_event(self):
        user1 = create_user(username='User1')
        user2 = create_user(username='User2')
        profile1 = create_profile(user=user2, tester=True)
        profile2 = create_profile(user=user1, boss=True)
        unit = create_unit(
            unit_name='Установка',
            unit_manager=profile,
            )
        start = datetime.datetime.now()
        end = datetime.datetime.now()

        print('time', start, end)
        eve = create_reservation(
            unit=unit,
            tester=profile1,
            owner=profile2,
            start_work=start,
            end_work=end
        )
        print('eve:', eve, dir(eve))

    # def setUp(self):
    #     pass
    
    # def test_1(self):
    #     self.create_unit_event()
