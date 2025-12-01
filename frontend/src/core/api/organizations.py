"""Organizations API endpoints."""
from typing import Dict, Any
from .client import APIClient


class OrganizationsAPI:
    """Organizations endpoints."""

    def __init__(self, client: APIClient):
        self.client = client

    def create_organization(
            self,
            name: str,
            code: str,
            primary_email: str,
    ) -> Dict[str, Any]:
        """Create new organization.

        Args:
            name: Organization name
            code: 8-character unique code (letters + numbers)
            primary_email: Primary admin email

        Returns:
            Created organization data with org_id
        """
        return self.client.post(
            "/organizations",
            json={
                "name": name,
                "code": code,
                "primary_email": primary_email,
            },
            include_auth=False,  # No auth needed for organization creation
        )
