from unittest.mock import patch

import pytest
from rest_framework.test import APIClient

from payouts.models import Payout


@pytest.mark.django_db
def test_create_payout_success():
    client = APIClient()
    payload = {
        "amount": "100.00",
        "currency": "RUB",
        "recipient_details": "Card 4111 1111 1111 1111",
        "description": "Test payout",
    }

    with patch("payouts.tasks.process_payout_task.delay"):
        response = client.post("/api/payouts/", payload, format="json")

    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == "100.00"
    assert data["currency"] == "RUB"
    assert data["status"] == Payout.Status.NEW


@pytest.mark.django_db
def test_celery_task_called_on_create():
    client = APIClient()
    payload = {
        "amount": "150.00",
        "currency": "RUB",
        "recipient_details": "Account 40817...",
    }

    with patch("payouts.tasks.process_payout_task.delay") as delay_mock:
        response = client.post("/api/payouts/", payload, format="json")

    assert response.status_code == 201
    delay_mock.assert_called_once()
