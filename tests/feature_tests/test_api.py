from requests_mock import Mocker
from fastapi.testclient import TestClient
from cyberfusion.PagerDutyVoysWebhook.settings import settings
from cyberfusion.PagerDutyVoysWebhook.api import app

from cyberfusion.PagerDutyVoysWebhook.pagerduty import BASE_URL

from cyberfusion.PagerDutyVoysWebhook.pagerduty import (
    NAME_METHOD_CONTACT_PHONE,
    NAME_METHOD_CONTACT_SMS,
)
from tests._helpers import generate_random_pagerduty_id

client = TestClient(app)


def test_voys_webhook_incorrect_secret_key() -> None:
    response = client.get("/voys-webhook", params={"secret_key": "wrong"})

    assert response.status_code == 401
    assert response.text == "status=NAK"


def test_voys_webhook_single_phone_contact_method(
    requests_mock: Mocker,
) -> None:
    schedule_id = generate_random_pagerduty_id()
    user_id = generate_random_pagerduty_id()

    contact_method_id_0 = generate_random_pagerduty_id()
    contact_method_id_1 = generate_random_pagerduty_id()

    single_on_call = {
        "oncalls": [
            {
                "escalation_policy": {
                    "id": settings.escalation_policy_id,
                    "type": "escalation_policy_reference",
                    "summary": "Subject Matter Experts",
                    "self": "https://api.pagerduty.com/escalation_policies/"
                    + settings.escalation_policy_id,
                    "html_url": "https://example.pagerduty.com/escalation_policies/"
                    + settings.escalation_policy_id,
                },
                "escalation_level": 1,
                "schedule": {
                    "id": schedule_id,
                    "type": "schedule_reference",
                    "summary": "Subject Matter Experts",
                    "self": "https://api.pagerduty.com/schedules/" + schedule_id,
                    "html_url": "https://example.pagerduty.com/schedules/"
                    + schedule_id,
                },
                "user": {
                    "id": user_id,
                    "type": "user_reference",
                    "summary": "John Doe",
                    "self": "https://api.pagerduty.com/users/" + user_id,
                    "html_url": "https://example.pagerduty.com/users/" + user_id,
                },
                "start": "2025-01-04T16:56:05Z",
                "end": "2025-04-23T04:55:46Z",
            }
        ],
        "limit": 25,
        "offset": 0,
        "more": False,
        "total": None,
    }

    single_phone_contact_method = {
        "contact_methods": [
            {
                "id": contact_method_id_0,
                "type": NAME_METHOD_CONTACT_PHONE,
                "summary": "Mobile",
                "self": "https://api.pagerduty.com/users/"
                + user_id
                + "/contact_methods/"
                + contact_method_id_0,
                "html_url": None,
                "label": "Mobile",
                "address": "611111111",
                "blacklisted": None,
                "country_code": 31,
            },
            {
                "id": contact_method_id_1,
                "type": NAME_METHOD_CONTACT_SMS,
                "summary": "Mobile",
                "self": "https://api.pagerduty.com/users/"
                + user_id
                + "/contact_methods/"
                + contact_method_id_1,
                "html_url": None,
                "label": "Mobile",
                "address": "622222222",
                "blacklisted": None,
                "country_code": 31,
                "enabled": True,
            },
        ],
        "total": 2,
    }

    requests_mock.get(BASE_URL + "/oncalls", json=single_on_call)
    requests_mock.get(
        BASE_URL + "/users/" + user_id + "/contact_methods",
        json=single_phone_contact_method,
    )

    response = client.get("/voys-webhook", params={"secret_key": settings.secret_key})

    phone_user_contact_methods = [
        c
        for c in single_phone_contact_method["contact_methods"]
        if c["type"] == NAME_METHOD_CONTACT_PHONE
    ]
    assert len(phone_user_contact_methods) == 1

    phone_user_contact_method = phone_user_contact_methods[0]

    country_code = str(phone_user_contact_method["country_code"])
    address = phone_user_contact_method["address"]

    assert response.status_code == 200
    assert response.text == "status=ACK&destination=%2B" + country_code + address


def test_voys_webhook_random_phone_contact_method(
    requests_mock: Mocker,
) -> None:
    schedule_id = generate_random_pagerduty_id()
    user_id = generate_random_pagerduty_id()

    contact_method_id_0 = generate_random_pagerduty_id()
    contact_method_id_1 = generate_random_pagerduty_id()
    contact_method_id_2 = generate_random_pagerduty_id()
    contact_method_id_3 = generate_random_pagerduty_id()

    single_on_call = {
        "oncalls": [
            {
                "escalation_policy": {
                    "id": settings.escalation_policy_id,
                    "type": "escalation_policy_reference",
                    "summary": "Subject Matter Experts",
                    "self": "https://api.pagerduty.com/escalation_policies/"
                    + settings.escalation_policy_id,
                    "html_url": "https://example.pagerduty.com/escalation_policies/"
                    + settings.escalation_policy_id,
                },
                "escalation_level": 1,
                "schedule": {
                    "id": schedule_id,
                    "type": "schedule_reference",
                    "summary": "Subject Matter Experts",
                    "self": "https://api.pagerduty.com/schedules/" + schedule_id,
                    "html_url": "https://example.pagerduty.com/schedules/"
                    + schedule_id,
                },
                "user": {
                    "id": user_id,
                    "type": "user_reference",
                    "summary": "John Doe",
                    "self": "https://api.pagerduty.com/users/" + user_id,
                    "html_url": "https://example.pagerduty.com/users/" + user_id,
                },
                "start": "2025-01-04T16:56:05Z",
                "end": "2025-04-23T04:55:46Z",
            }
        ],
        "limit": 25,
        "offset": 0,
        "more": False,
        "total": None,
    }

    multiple_phone_contact_methods = {
        "contact_methods": [
            {
                "id": contact_method_id_0,
                "type": NAME_METHOD_CONTACT_PHONE,
                "summary": "Mobile",
                "self": "https://api.pagerduty.com/users/"
                + user_id
                + "/contact_methods/"
                + contact_method_id_0,
                "html_url": None,
                "label": "Mobile",
                "address": "633333333",
                "blacklisted": None,
                "country_code": 31,
            },
            {
                "id": contact_method_id_1,
                "type": NAME_METHOD_CONTACT_PHONE,
                "summary": "Mobile",
                "self": "https://api.pagerduty.com/users/"
                + user_id
                + "/contact_methods/"
                + contact_method_id_1,
                "html_url": None,
                "label": "Mobile",
                "address": "644444444",
                "blacklisted": None,
                "country_code": 31,
            },
            {
                "id": contact_method_id_2,
                "type": NAME_METHOD_CONTACT_SMS,
                "summary": "Mobile",
                "self": "https://api.pagerduty.com/users/"
                + user_id
                + "/contact_methods/"
                + contact_method_id_2,
                "html_url": None,
                "label": "Mobile",
                "address": "655555555",
                "blacklisted": None,
                "country_code": 31,
                "enabled": True,
            },
            {
                "id": contact_method_id_3,
                "type": NAME_METHOD_CONTACT_SMS,
                "summary": "Mobile",
                "self": "https://api.pagerduty.com/users/"
                + user_id
                + "/contact_methods/"
                + contact_method_id_3,
                "html_url": None,
                "label": "Mobile",
                "address": "666666666",
                "blacklisted": None,
                "country_code": 31,
                "enabled": True,
            },
        ],
        "total": 4,
    }

    requests_mock.get(BASE_URL + "/oncalls", json=single_on_call)
    requests_mock.get(
        BASE_URL + "/users/" + user_id + "/contact_methods",
        json=multiple_phone_contact_methods,
    )

    phone_user_contact_methods = [
        c
        for c in multiple_phone_contact_methods["contact_methods"]
        if c["type"] == NAME_METHOD_CONTACT_PHONE
    ]
    assert len(phone_user_contact_methods) > 1

    seen_phone_numbers = []

    base_text = "status=ACK&destination=%2B"

    # Test randomness of phone numbers. Having retrieved them 10 times, all of
    # them should have been picked at least once.

    for i in range(10):
        response = client.get(
            "/voys-webhook", params={"secret_key": settings.secret_key}
        )

        assert response.status_code == 200
        assert response.text.startswith(base_text)

        phone_number = response.text[len(base_text) :]

        seen_phone_numbers.append(phone_number)

    for phone_number in phone_user_contact_methods:
        country_code = str(phone_number["country_code"])
        address = phone_number["address"]

        assert country_code + address in seen_phone_numbers


def test_voys_webhook_random_on_call(
    requests_mock: Mocker,
) -> None:
    schedule_id_0 = generate_random_pagerduty_id()
    schedule_id_1 = generate_random_pagerduty_id()

    user_id_0 = generate_random_pagerduty_id()
    user_id_1 = generate_random_pagerduty_id()

    contact_method_id_0 = generate_random_pagerduty_id()
    contact_method_id_1 = generate_random_pagerduty_id()

    multiple_on_calls = {
        "oncalls": [
            {
                "escalation_policy": {
                    "id": settings.escalation_policy_id,
                    "type": "escalation_policy_reference",
                    "summary": "Subject Matter Experts",
                    "self": "https://api.pagerduty.com/escalation_policies/"
                    + settings.escalation_policy_id,
                    "html_url": "https://example.pagerduty.com/escalation_policies/"
                    + settings.escalation_policy_id,
                },
                "escalation_level": 1,
                "schedule": {
                    "id": schedule_id_0,
                    "type": "schedule_reference",
                    "summary": "Subject Matter Experts",
                    "self": "https://api.pagerduty.com/schedules/" + schedule_id_0,
                    "html_url": "https://example.pagerduty.com/schedules/"
                    + schedule_id_0,
                },
                "user": {
                    "id": user_id_0,
                    "type": "user_reference",
                    "summary": "John Doe",
                    "self": "https://api.pagerduty.com/users/" + user_id_0,
                    "html_url": "https://example.pagerduty.com/users/" + user_id_0,
                },
                "start": "2025-01-04T16:56:05Z",
                "end": "2025-04-23T04:55:46Z",
            },
            {
                "escalation_policy": {
                    "id": settings.escalation_policy_id,
                    "type": "escalation_policy_reference",
                    "summary": "Subject Matter Experts",
                    "self": "https://api.pagerduty.com/escalation_policies/"
                    + settings.escalation_policy_id,
                    "html_url": "https://example.pagerduty.com/escalation_policies/"
                    + settings.escalation_policy_id,
                },
                "escalation_level": 1,
                "schedule": {
                    "id": schedule_id_1,
                    "type": "schedule_reference",
                    "summary": "Subject Matter Experts",
                    "self": "https://api.pagerduty.com/schedules/" + schedule_id_1,
                    "html_url": "https://example.pagerduty.com/schedules/"
                    + schedule_id_1,
                },
                "user": {
                    "id": user_id_1,
                    "type": "user_reference",
                    "summary": "Jane Doe",
                    "self": "https://api.pagerduty.com/users/" + user_id_1,
                    "html_url": "https://example.pagerduty.com/users/" + user_id_1,
                },
                "start": "2025-01-04T16:56:05Z",
                "end": "2025-04-23T04:55:46Z",
            },
        ],
        "limit": 25,
        "offset": 0,
        "more": False,
        "total": None,
    }

    single_phone_contact_method_0 = {
        "contact_methods": [
            {
                "id": contact_method_id_0,
                "type": NAME_METHOD_CONTACT_PHONE,
                "summary": "Mobile",
                "self": "https://api.pagerduty.com/users/"
                + user_id_0
                + "/contact_methods/"
                + contact_method_id_0,
                "html_url": None,
                "label": "Mobile",
                "address": "611111111",
                "blacklisted": None,
                "country_code": 31,
            },
        ],
        "total": 2,
    }

    single_phone_contact_method_1 = {
        "contact_methods": [
            {
                "id": contact_method_id_1,
                "type": NAME_METHOD_CONTACT_PHONE,
                "summary": "Mobile",
                "self": "https://api.pagerduty.com/users/"
                + user_id_1
                + "/contact_methods/"
                + contact_method_id_1,
                "html_url": None,
                "label": "Mobile",
                "address": "622222222",
                "blacklisted": None,
                "country_code": 31,
            },
        ],
        "total": 2,
    }

    requests_mock.get(BASE_URL + "/oncalls", json=multiple_on_calls)
    requests_mock.get(
        BASE_URL + "/users/" + user_id_0 + "/contact_methods",
        json=single_phone_contact_method_0,
    )
    requests_mock.get(
        BASE_URL + "/users/" + user_id_1 + "/contact_methods",
        json=single_phone_contact_method_1,
    )

    phone_user_contact_methods_0 = [
        c
        for c in single_phone_contact_method_0["contact_methods"]
        if c["type"] == NAME_METHOD_CONTACT_PHONE
    ]
    assert len(phone_user_contact_methods_0) == 1

    phone_user_contact_methods_1 = [
        c
        for c in single_phone_contact_method_1["contact_methods"]
        if c["type"] == NAME_METHOD_CONTACT_PHONE
    ]
    assert len(phone_user_contact_methods_1) == 1

    seen_phone_numbers = []

    base_text = "status=ACK&destination=%2B"

    # Test randomness of on-calls via phone numbers. Having retrieved them 10
    # times, all of them should have been picked at least once.

    for i in range(10):
        response = client.get(
            "/voys-webhook", params={"secret_key": settings.secret_key}
        )

        assert response.status_code == 200
        assert response.text.startswith(base_text)

        phone_number = response.text[len(base_text) :]

        seen_phone_numbers.append(phone_number)

    for phone_number in phone_user_contact_methods_0 + phone_user_contact_methods_1:
        country_code = str(phone_number["country_code"])
        address = phone_number["address"]

        assert country_code + address in seen_phone_numbers
