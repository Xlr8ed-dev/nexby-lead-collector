import datetime
import decimal
import uuid

from django.db import connection
from django.conf import settings
from leads.models import GoogleSheetSyncStatus
from leads.utility.google_sheets import get_gsheet_client, get_or_create_sheet

TABLES = ["contact_requests", "questions", "submissions"]
PRIMARY_KEYS = {
    "contact_requests": "id",
    "submissions": "id",
    "questions": "q_uid",
}


def serialize_value(value):
    if value is None:
        return ""
    if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        return value.isoformat()
    if isinstance(value, decimal.Decimal):
        return float(value)
    if isinstance(value, uuid.UUID):
        return str(value)
    return value


def fetch_new_rows(table, last_id):
    pk = PRIMARY_KEYS.get(table, "id")  # default to "id" if not found
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT * FROM public."{table}" WHERE "{pk}" > %s ORDER BY "{pk}" ASC',
            [last_id],
        )
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    return columns, rows


def sync_table(table_name):
    sync_obj, _ = GoogleSheetSyncStatus.objects.get_or_create(
        table_name=table_name
    )

    columns, rows = fetch_new_rows(table_name, sync_obj.last_synced_id)

    if not rows:
        return

    client = get_gsheet_client()
    spreadsheet = client.open_by_key(settings.GOOGLE_SPREADSHEET_ID)
    worksheet = get_or_create_sheet(
        spreadsheet,
        sheet_name=table_name,
        headers=columns
    )

    values = [
        [serialize_value(v) for v in row]
        for row in rows
    ]
    worksheet.append_rows(values, value_input_option="RAW")

    pk = PRIMARY_KEYS.get(table_name, "id")
    sync_obj.last_synced_id = max(row[columns.index(pk)] for row in rows)
    sync_obj.save()


def sync_all_tables():
    for table in TABLES:
        sync_table(table)
