"""Helpers for Voys webhooks.

Voys documentation: https://help.voys.nl/integraties-koppelingen-webhooks/webhooks
"""

import logging
import urllib.parse


def construct_webhook_response_destination(destination: str) -> str:
    """Construct webhook response with destination."""
    parameters = {"status": "ACK", "destination": destination}

    response = urllib.parse.urlencode(parameters)

    logging.info("Webhook response: %s", response)

    return response


def construct_webhook_response_wrong_input() -> str:
    """Construct webhook response signalling wrong input."""
    parameters = {"status": "NAK"}

    response = urllib.parse.urlencode(parameters)

    logging.info("Webhook response: %s", response)

    return response
