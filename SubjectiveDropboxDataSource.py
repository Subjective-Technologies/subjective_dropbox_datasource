import os
from typing import List

from subjective_abstract_data_source_package import SubjectiveDataSource
from brainboost_data_source_logger_package.BBLogger import BBLogger
from brainboost_rclone_oauth_package import DropboxOAuth

class SubjectiveDropboxDataSource(SubjectiveDataSource):
    def __init__(self, name=None, session=None, dependency_data_sources=None, subscribers=None, params=None):
        super().__init__(
            name=name,
            session=session,
            dependency_data_sources=dependency_data_sources or [],
            subscribers=subscribers,
            params=params,
        )
        self.params = params or {}

    def fetch(self):
        params = self.params or {}
        client_id = (params.get("client_id") or params.get("app_key") or "").strip()
        if not client_id:
            raise ValueError("Dropbox client_id is required.")

        client_secret = (params.get("client_secret") or "").strip() or None
        redirect_host = (params.get("redirect_host") or "127.0.0.1").strip()
        redirect_port = int(params.get("redirect_port") or 53682)

        scopes_raw = (params.get("scopes") or "").strip()
        scopes: List[str] = []
        if scopes_raw:
            scopes = [s.strip() for s in scopes_raw.replace(",", " ").split() if s.strip()]

        action = (params.get("oauth_action") or "").strip().lower()
        access_token = (params.get("access_token") or "").strip()
        if action not in ("authorize", "auth", "login") and access_token:
            return {"access_token": access_token}

        oauth = DropboxOAuth(
            client_id=client_id,
            client_secret=client_secret,
            scopes=scopes or None,
            redirect_host=redirect_host,
            redirect_port=redirect_port,
            logger=BBLogger.log,
        )
        result = oauth.authorize()
        return {
            "access_token": result.access_token,
            "refresh_token": result.refresh_token,
            "expires_in": result.expires_in,
            "token_type": result.token_type,
            "scope": result.scope,
        }

    def get_icon(self) -> str:
        icon_path = os.path.join(os.path.dirname(__file__), "icon.svg")
        try:
            with open(icon_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            BBLogger.log(f"Error reading icon file: {e}")
            return ""

    def get_connection_data(self) -> dict:
        return {
            "connection_type": "DROPBOX",
            "fields": [
                {
                    "name": "client_id",
                    "label": "Dropbox App Key (client_id)",
                    "type": "text",
                    "required": True,
                },
                {
                    "name": "client_secret",
                    "label": "Dropbox App Secret (optional)",
                    "type": "password",
                },
                {
                    "name": "scopes",
                    "label": "Scopes (space or comma separated)",
                    "type": "text",
                    "placeholder": "files.metadata.read files.content.read",
                },
                {
                    "name": "redirect_host",
                    "label": "Redirect Host",
                    "type": "text",
                    "default": "127.0.0.1",
                },
                {
                    "name": "redirect_port",
                    "label": "Redirect Port",
                    "type": "number",
                    "default": 53682,
                },
                {
                    "name": "oauth_action",
                    "label": "OAuth Action (set to authorize to generate token)",
                    "type": "text",
                    "placeholder": "authorize",
                },
                {
                    "name": "access_token",
                    "label": "Access Token (output)",
                    "type": "text",
                },
                {
                    "name": "refresh_token",
                    "label": "Refresh Token (output)",
                    "type": "text",
                },
            ],
        }
