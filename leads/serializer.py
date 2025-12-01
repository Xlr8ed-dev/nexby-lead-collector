from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from leads.models import ContactUs


class ContactUsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    company_name = serializers.CharField(required=True)
    company_email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=ContactUs.objects.all(),
                message="Email already exists",
            )
        ],
    )
    mobile_number = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=ContactUs.objects.all(),
                message="Mobile number already exists",
            ),
            RegexValidator(
                regex=r"^\+?\d{10,15}$",
                message="Mobile number must contain 10–15 digits and may start with +.",
            ),
        ],
    )
    plan_details = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    country_code = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, max_length=10
    )
    is_event_management = serializers.BooleanField(required=False, default=False)
    lead_capture_method = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    annual_exhibitions = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    submission_timestamp = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = ContactUs
        fields = [
            "full_name",
            "company_name",
            "company_email",
            "mobile_number",
            "plan_details",
            "country_code",
            "is_event_management",
            "lead_capture_method",
            "annual_exhibitions",
            "submission_timestamp",
        ]

    def to_internal_value(self, data):
        # Map 'email' to 'company_email' if 'email' is provided
        if "email" in data and "company_email" not in data:
            data = data.copy()  # Create a mutable copy
            data["company_email"] = data.pop("email")
        return super().to_internal_value(data)

    def create(self, validated_data):
        contact = ContactUs.objects.create(**validated_data)
        return contact