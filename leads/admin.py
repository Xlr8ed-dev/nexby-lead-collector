from django.contrib import admin

from leads.models import ContactUs


class ContactUsAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "company_email",
        "mobile_number",
        "plan_details",
        "country_code",
        "is_event_management",
        "lead_capture_method",
        "annual_exhibitions",
        "created_at",
    )
    search_fields = (
        "full_name",
        "company_email",
        "mobile_number",
        "plan_details",
        "country_code",
        "is_event_management",
        "lead_capture_method",
        "annual_exhibitions",
        "created_at",
    )


admin.site.register(ContactUs, ContactUsAdmin)
