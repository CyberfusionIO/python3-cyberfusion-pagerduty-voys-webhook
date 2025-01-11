import requests
import random

BASE_URL = "https://api.pagerduty.com"

NAME_METHOD_CONTACT_PHONE = "phone_contact_method"
NAME_METHOD_CONTACT_SMS = "sms_contact_method"


class PagerDutyAPI:
    """Class to interact with PagerDuty API.

    Official PagerDuty Python library isn't used, as it's absent from the Debian
    repositories, and not strictly necessary.
    """

    def __init__(self, api_key: str) -> None:
        """Set attributes."""
        self.api_key = api_key

    @property
    def headers(self) -> dict:
        """Get HTTP request headers."""
        return {"Authorization": "Token token=" + self.api_key}

    def get_on_calls(self, escalation_policy_id: int) -> dict:
        """Get on-calls."""
        request = requests.get(
            BASE_URL + "/oncalls",
            headers=self.headers,
            params={"escalation_policy_ids[]": escalation_policy_id},
        )

        request.raise_for_status()

        return request.json()

    def get_random_on_call(self, escalation_policy_id: int) -> dict:
        """Get random on-call."""
        on_calls = self.get_on_calls(escalation_policy_id)

        on_call = random.choice(on_calls["oncalls"])

        return on_call

    def get_user_contact_methods(self, user_id: str) -> dict:
        """Get user contact methods."""
        request = requests.get(
            BASE_URL + f"/users/{user_id}/contact_methods", headers=self.headers
        )

        request.raise_for_status()

        return request.json()

    def get_user_phone_contact_methods(self, user_id: str) -> list[dict]:
        """Get user phone contact methods."""
        user_contact_methods = self.get_user_contact_methods(user_id)

        phone_contact_methods = [
            contact_method
            for contact_method in user_contact_methods["contact_methods"]
            if contact_method["type"] == NAME_METHOD_CONTACT_PHONE
        ]

        return phone_contact_methods

    def get_random_phone_contact_method(self, user_id: str) -> dict:
        """Get random phone contact method."""
        phone_contact_methods = self.get_user_phone_contact_methods(user_id)

        phone_contact_method = random.choice(phone_contact_methods)

        return phone_contact_method