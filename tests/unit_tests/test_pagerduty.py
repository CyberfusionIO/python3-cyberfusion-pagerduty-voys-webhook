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
