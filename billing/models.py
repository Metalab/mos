from django.db import models


class Invoice(models.Model):
    number = models.PositiveIntegerField(null=False, unique_for_year="date")
    invoice_recipient = models.TextField(null=False)
    invoice_address = models.TextField(null=False)
    date = models.DateField(null=False)
    invoice_mail_recipient = models.EmailField()
    invoice_mailed_at = models.DateTimeField()

    class Admin:
        pass


class InoviceItem(models.Model):
    invoice = models.ForeignKey(Invoice, null=False,
                                edit_inline=models.TABULAR, core=True)
    text = models.TextField(null=False, core=True)
    value = models.DecimalField(null=False, decimal_places=2, max_digits=7,
                                core=True)
    order = models.PositiveIntegerField(null=False, core=True)

    class Admin:
        pass
