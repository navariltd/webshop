import frappe
from frappe.utils import get_url

from erpnext.accounts.doctype.payment_request.payment_request import (
    PaymentRequest as OriginalPaymentRequest,
)


class PaymentRequest(OriginalPaymentRequest):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from erpnext.accounts.doctype.subscription_plan_detail.subscription_plan_detail import (
            SubscriptionPlanDetail,
        )
        from frappe.types import DF

        account: DF.ReadOnly | None
        amended_from: DF.Link | None
        bank: DF.Link | None
        bank_account: DF.Link | None
        bank_account_no: DF.ReadOnly | None
        branch_code: DF.ReadOnly | None
        company: DF.Link | None
        cost_center: DF.Link | None
        currency: DF.Link | None
        email_to: DF.Data | None
        grand_total: DF.Currency
        iban: DF.ReadOnly | None
        is_a_subscription: DF.Check
        make_sales_invoice: DF.Check
        message: DF.Text | None
        mode_of_payment: DF.Link | None
        mute_email: DF.Check
        naming_series: DF.Literal["ACC-PRQ-.YYYY.-"]
        outstanding_amount: DF.Currency
        party: DF.DynamicLink | None
        party_account_currency: DF.Link | None
        party_name: DF.Data | None
        party_type: DF.Link | None
        payment_account: DF.ReadOnly | None
        payment_channel: DF.Literal["", "Email", "Phone"]
        payment_gateway: DF.ReadOnly | None
        payment_gateway_account: DF.Link | None
        payment_order: DF.Link | None
        payment_request_type: DF.Literal["Outward", "Inward"]
        payment_url: DF.Data | None
        phone_number: DF.Data | None
        print_format: DF.Literal[None]
        project: DF.Link | None
        reference_doctype: DF.Link | None
        reference_name: DF.DynamicLink | None
        status: DF.Literal[
            "",
            "Draft",
            "Requested",
            "Initiated",
            "Partially Paid",
            "Payment Ordered",
            "Paid",
            "Failed",
            "Cancelled",
        ]
        subject: DF.Data | None
        subscription_plans: DF.Table[SubscriptionPlanDetail]
        swift_number: DF.ReadOnly | None
        transaction_date: DF.Date | None
    # end: auto-generated types

    def on_payment_authorized(self, status=None):
        if not status:
            return

        if status not in ("Authorized", "Completed"):
            return

        if not hasattr(frappe.local, "session"):
            return

        if frappe.local.session.user == "Guest":
            return

        if self.payment_channel == "Phone":
            return

        cart_settings = frappe.get_doc("Webshop Settings")

        if not cart_settings.enabled:
            return

        success_url = cart_settings.payment_success_url
        redirect_to = get_url("/orders/{0}".format(self.reference_name))

        if success_url:
            redirect_to = (
                {
                    "Orders": "/orders",
                    "Invoices": "/invoices",
                    "My Account": "/me",
                }
            ).get(success_url, "/me")

        self.set_as_paid()

        return redirect_to

    @staticmethod
    def get_gateway_details(args):
        if args.order_type != "Shopping Cart":
            return super().get_gateway_details(args)

        cart_settings = frappe.get_doc("Webshop Settings")
        gateway_account = cart_settings.payment_gateway_account
        return super().get_payment_gateway_account(gateway_account)
