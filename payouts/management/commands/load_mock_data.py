import csv
from decimal import Decimal
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from payouts.models import Payout


def load_csv(path: Path, required_cols: list[str]) -> list[dict]:
    if not path.exists():
        raise CommandError(f"CSV файл не найден: {path}")
    rows: list[dict] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise CommandError(f"{path.name}: пустой или без заголовка")
        missing = [c for c in required_cols if c not in reader.fieldnames]
        if missing:
            raise CommandError(f"{path.name}: отсутствуют колонки: {missing}")
        for row in reader:
            rows.append({
                k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()
            })
    return rows


class Command(BaseCommand):
    help = "Загружает мок-данные заявок на выплату из CSV."

    def add_arguments(self, parser):
        parser.add_argument(
            "--data-dir",
            default="payouts/management/data",
            help="Каталог с CSV файлами (по умолчанию payouts/management/data)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        data_dir = Path(options["data_dir"])
        payouts_csv = load_csv(
            data_dir / "payouts.csv",
            ["external_id", "amount", "currency", "recipient_details", "status"],
        )

        created = 0
        updated = 0

        for row in payouts_csv:
            processed_at = self._parse_datetime(row.get("processed_at") or "")
            description = row.get("description") or ""
            error_message = row.get("error_message") or None

            defaults = {
                "amount": Decimal(row["amount"]),
                "currency": row["currency"],
                "recipient_details": row["recipient_details"],
                "status": row["status"],
                "description": description,
                "error_message": error_message,
                "processed_at": processed_at,
            }

            payout, was_created = Payout.objects.update_or_create(
                external_id=row["external_id"], defaults=defaults
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Мок-данные загружены: создано {created}, обновлено {updated}"
            )
        )

    def _parse_datetime(self, value: str):
        if not value:
            return None
        dt = parse_datetime(value)
        if dt is None:
            raise CommandError(f"Некорректный datetime: {value}")
        if timezone.is_naive(dt):
            return timezone.make_aware(dt)
        return dt
