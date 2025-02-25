from datetime import date

from juntagrico.entity.subs import Subscription
from test.util.test import JuntagricoTestCase


class AssignmentTests(JuntagricoTestCase):
    year = 2022
    activation_date = date(day=1, month=1, year=year)

    def setUp(self):
        super().setUp()
        self.sub_trial_type = self.create_sub_type(self.sub_size, trial_days=30)
        self.subs = [
            # sub in second half of the year
            self.create_sub(self.depot, date(day=1, month=7, year=self.year), parts=[self.sub_type]),
            # sub in first half of the year
            self.create_sub(self.depot, self.activation_date, deactivation_date=date(day=30, month=6, year=self.year), parts=[self.sub_type]),
            # trial sub ongoing
            self.create_sub(self.depot, self.activation_date, [self.sub_trial_type]),
            # trial sub shorter than planned
            self.create_sub(self.depot, self.activation_date, deactivation_date=date(day=15, month=1, year=self.year), parts=[self.sub_trial_type]),
            # trial sub at the end of the year
            self.create_sub(self.depot, date(day=15, month=12, year=self.year), [self.sub_trial_type]),
            # trial sub starting last year
            self.create_sub(self.depot, date(day=15, month=12, year=self.year - 1), [self.sub_trial_type]),
            # ordered, not activated sub
            self.create_sub(self.depot, parts=[self.sub_type]),
            # multiple parts
            self.create_sub(self.depot, self.activation_date, parts=[self.sub_type, self.sub_type]),
        ]

    def testRequiredAssignments(self):
        # get assignments for entire year.
        subs = Subscription.objects.annotate_required_assignments(self.activation_date, date(self.year, 12, 31)).filter(pk__in=self.subs).distinct()
        # sub in second half of the year
        self.assertEqual(subs[0].required_assignments, 5)
        self.assertEqual(subs[0].required_core_assignments, 2)
        # sub in first half of the year
        self.assertEqual(subs[1].required_assignments, 5)
        self.assertEqual(subs[1].required_core_assignments, 1)  # first 6 months or the year are a bit shorter
        # trial sub ongoing
        self.assertEqual(subs[2].required_assignments, 10)
        self.assertEqual(subs[2].required_core_assignments, 3)
        # trial sub shorter than normal trial period
        self.assertEqual(subs[3].required_assignments, 5)
        self.assertEqual(subs[3].required_core_assignments, 2)
        # trial sub at the end of the year
        self.assertEqual(subs[4].required_assignments, 6)  # 17/30 rounded
        self.assertEqual(subs[4].required_core_assignments, 2)
        # trial sub starting last year
        self.assertEqual(subs[5].required_assignments, 4)  # 13/30 rounded
        self.assertEqual(subs[5].required_core_assignments, 1)
        # ordered, not activated sub
        self.assertEqual(subs[6].required_assignments, 0)
        self.assertEqual(subs[6].required_core_assignments, 0)
        # multiple parts
        self.assertEqual(subs[7].required_assignments, 20)
        self.assertEqual(subs[7].required_core_assignments, 6)
