from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.models import modelform_factory
from django.test import TestCase

from members.models import BankCollectionMode
from members.models import PaymentInfo

VALID_IBAN = "AT611904300234573201"


class PaymentInfoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester")
        self.mode = BankCollectionMode.objects.create(
            name="monthly", num_month=1
        )

    def _payment_info(self, **overrides):
        values = {
            "user": self.user,
            "bank_collection_mode": self.mode,
            "bank_collection_allowed": True,
            "bank_account_owner": "Max Mustermann",
            "bank_account_iban": VALID_IBAN,
            "bank_account_mandate_reference": "ref-1",
            "bank_account_date_of_signing": date(2026, 1, 1),
        }
        values.update(overrides)
        return PaymentInfo(**values)

    def test_collection_not_allowed_without_bank_details_is_valid(self):
        info = self._payment_info(
            bank_collection_allowed=False,
            bank_account_owner="",
            bank_account_iban="",
            bank_account_mandate_reference="",
            bank_account_date_of_signing=None,
        )
        info.full_clean()  # does not raise

    def test_collection_allowed_with_complete_bank_details_is_valid(self):
        info = self._payment_info()
        info.full_clean()  # does not raise

    def test_collection_allowed_with_missing_bank_details_is_invalid(self):
        info = self._payment_info(
            bank_account_owner="",
            bank_account_iban="",
            bank_account_mandate_reference="",
            bank_account_date_of_signing=None,
        )
        with self.assertRaises(ValidationError) as ctx:
            info.full_clean()
        self.assertEqual(
            set(ctx.exception.message_dict),
            {
                "bank_account_owner",
                "bank_account_iban",
                "bank_account_mandate_reference",
                "bank_account_date_of_signing",
            },
        )

    def test_collection_allowed_reports_only_missing_fields(self):
        info = self._payment_info(bank_account_iban="")
        with self.assertRaises(ValidationError) as ctx:
            info.full_clean()
        self.assertEqual(
            set(ctx.exception.message_dict), {"bank_account_iban"}
        )

    def test_admin_form_rejects_missing_bank_details(self):
        form = modelform_factory(PaymentInfo, fields="__all__")(
            data={
                "user": self.user.pk,
                "bank_collection_mode": self.mode.pk,
                "bank_collection_allowed": True,
                "bank_account_owner": "",
                "bank_account_iban": "",
                "bank_account_bic": "",
                "bank_name": "",
                "bank_account_mandate_reference": "",
                "bank_account_date_of_signing": "",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("bank_account_owner", form.errors)
        self.assertIn("bank_account_iban", form.errors)
        self.assertIn("bank_account_date_of_signing", form.errors)

    def test_admin_form_accepts_complete_bank_details(self):
        form = modelform_factory(PaymentInfo, fields="__all__")(
            data={
                "user": self.user.pk,
                "bank_collection_mode": self.mode.pk,
                "bank_collection_allowed": True,
                "bank_account_owner": "Max Mustermann",
                "bank_account_iban": VALID_IBAN,
                "bank_account_bic": "GIBAATWWXXX",
                "bank_name": "Erste Bank",
                "bank_account_mandate_reference": "ref-1",
                "bank_account_date_of_signing": "2026-01-01",
            }
        )
        self.assertTrue(form.is_valid())
