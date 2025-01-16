from _pytest.logging import LogCaptureFixture
import logging

from cyberfusion.PagerDutyVoysWebhook.voys import (
    construct_webhook_response_destination,
    construct_webhook_response_wrong_input,
)

logger = logging.getLogger(__name__)


def test_construct_webhook_response_destination_log(caplog: LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO):
        construct_webhook_response_destination("+3111111111")

    assert "Webhook response: status=ACK&destination=%2B3111111111" in caplog.text


def test_construct_webhook_response_wrong_input_log(caplog: LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO):
        construct_webhook_response_wrong_input()

    assert "Webhook response: status=NAK" in caplog.text
