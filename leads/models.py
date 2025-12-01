from django.db import models


class ContactUs(models.Model):
    full_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Full Name",
        help_text="Enter the full name of the contact person.",
    )
    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Company Name",
        help_text="Enter the name of the company.",
    )
    company_email = models.EmailField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="Company Email",
        help_text="Enter the company's email address.",
    )
    mobile_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Mobile Number",
        help_text="Enter the contact person's mobile number.",
    )
    plan_details = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Plan Details",
        help_text="Enter the plan details (e.g., Pro, Basic).",
    )
    country_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Country Code",
        help_text="Enter the country code (e.g., 91).",
    )
    is_event_management = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Is Event Management",
        help_text="Enter the country code (e.g., 91).",
    )
    lead_capture_method = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Lead Capture Method",
        help_text="Enter the lead capture method (e.g., website, email).",
    )
    annual_exhibitions = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Annual Exhibitions",
        help_text="Enter the number of annual exhibitions.",
    )
    submission_timestamp = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Submission Timestamp",
        help_text="Enter the submission timestamp.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created Date",
        help_text="The date and time when the contact was created.",
    )

    def __str__(self):
        return f"{self.full_name} - {self.company_email} - {self.company_name} - {self.mobile_number} - {self.plan_details} - {self.country_code}"
