from celery import shared_task

from leads.utility.sync_to_gsheets import sync_all_tables


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 10})
def sync_db_to_google_sheets(self):
    sync_all_tables()
