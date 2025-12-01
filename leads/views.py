import os
import sys

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny

from leads.serializer import ContactUsSerializer
from utility.custom_response import create_response
from utility.date_time_util import get_date_time_dict_in_ist
from utility.serializer_error import serializer_error
from utility.write_data_to_google_sheet import write_data_to_google_sheet


# Create your views here.
class ContactusViewset(viewsets.ViewSet):
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [
        AllowAny,
    ]

    def Contact(self, request):
        try:
            serializer = ContactUsSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                company_email = user.company_email
                full_name = user.full_name
                company_name = user.company_name
                mobile_number = user.mobile_number
                plan_details = user.plan_details or ""
                country_code = user.country_code or ""
                is_event_management = user.is_event_management
                lead_capture_method = user.lead_capture_method or ""
                annual_exhibitions = user.annual_exhibitions or ""
                created_at = user.submission_timestamp or user.created_at
                data_to_write = [
                    [
                        full_name,
                        company_email,
                        mobile_number,
                        company_name,
                        plan_details,
                        country_code,
                        is_event_management,
                        lead_capture_method,
                        annual_exhibitions,
                        user_time["date"],
                        user_time["time"],
                    ]
                    for user_time in [
                        get_date_time_dict_in_ist(
                            datetime_utc_object=created_at, noon_format=True
                        )
                    ]
                ]
                sheet_name = "nexby_contact_us"
                spreadsheet_name = "Hr_Registration_Data"
                header = [
                    "full name",
                    "company email",
                    "Mobile Number",
                    "company name",
                    "Plan Details",
                    "Country Code",
                    "Is Event Management",
                    "Lead Capture Method",
                    "Annual Exhibitions",
                    "Created Date",
                    "Created Time",
                ]
                success_google_sheet, message_google_sheet = write_data_to_google_sheet(
                    sheet_name=sheet_name,
                    spreadsheet_name=spreadsheet_name,
                    header=header,
                    data=data_to_write,
                )
                if not success_google_sheet:
                    return create_response(
                        status.HTTP_500_INTERNAL_SERVER_ERROR,
                        errors=message_google_sheet,
                        message=message_google_sheet,
                    )
                return create_response(
                    status.HTTP_201_CREATED,
                    serializer.data,
                    message="contact register was successful.",
                )
            else:
                return create_response(
                    status.HTTP_400_BAD_REQUEST,
                    errors=serializer_error(serializer.errors),
                )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return create_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                errors="Internal server errors.",
                message=str(e),
            )
