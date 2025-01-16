from _pytest.logging import LogCaptureFixture
import logging

from requests_mock import Mocker

from cyberfusion.PagerDutyVoysWebhook.pagerduty import PagerDutyAPI

from cyberfusion.PagerDutyVoysWebhook.pagerduty import BASE_URL

from cyberfusion.PagerDutyVoysWebhook.settings import settings
from tests._helpers import generate_random_pagerduty_id

logger = logging.getLogger(__name__)


def test_get_user_contact_methods_log(
    caplog: LogCaptureFixture,
    requests_mock: Mocker,
) -> None:
    user_id = generate_random_pagerduty_id()

    requests_mock.get(
        BASE_URL + "/users/" + user_id + "/contact_methods",
        json={"contact_methods": []},
    )

    with caplog.at_level(logging.DEBUG):
        PagerDutyAPI(api_key=settings.api_key).get_user_contact_methods(user_id)

    assert "PagerDuty contact methods response: {'contact_methods': []}" in caplog.text


def test_get_on_calls_log(
    caplog: LogCaptureFixture,
    requests_mock: Mocker,
) -> None:
    requests_mock.get(BASE_URL + "/oncalls", json={"oncalls": []})

    with caplog.at_level(logging.DEBUG):
        PagerDutyAPI(api_key=settings.api_key).get_on_calls(
            escalation_policy_id=settings.escalation_policy_id
        )

    assert "PagerDuty on-calls response: {'oncalls': []}" in caplog.text


def test_get_random_on_call_escalation_policy_ne_1_ignored(
    requests_mock: Mocker,
) -> None:
    schedule_id_0 = generate_random_pagerduty_id()
    schedule_id_1 = generate_random_pagerduty_id()

    user_id_0 = generate_random_pagerduty_id()
    user_id_1 = generate_random_pagerduty_id()

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
                "escalation_level": 2,
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

    requests_mock.get(BASE_URL + "/oncalls", json=multiple_on_calls)

    seen_on_calls = []

    for i in range(10):
        seen_on_calls.append(
            PagerDutyAPI(api_key=settings.api_key).get_random_on_call(
                escalation_policy_id=settings.escalation_policy_id
            )
        )

    for seen_on_call in seen_on_calls:
        assert seen_on_call["escalation_level"] == 1
