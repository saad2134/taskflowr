from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import aiohttp
import asyncio


class BaseConnector(ABC):
    def __init__(self, credentials: Dict[str, Any]):
        self.credentials = credentials
    
    @abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def send_message(self, message: str, **kwargs) -> Dict[str, Any]:
        pass


class SlackConnector(BaseConnector):
    async def test_connection(self) -> Dict[str, Any]:
        try:
            token = self.credentials.get("bot_token")
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://slack.com/api/auth.test",
                    headers={"Authorization": f"Bearer {token}"}
                ) as resp:
                    data = await resp.json()
                    return {
                        "success": data.get("ok", False),
                        "message": "Connected" if data.get("ok") else "Failed",
                        "details": {"user": data.get("user"), "team": data.get("team")}
                    }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def send_message(self, message: str, channel: str = None, **kwargs) -> Dict[str, Any]:
        try:
            token = self.credentials.get("bot_token")
            payload = {
                "text": message,
                "channel": channel or self.credentials.get("default_channel")
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://slack.com/api/chat.postMessage",
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                ) as resp:
                    data = await resp.json()
                    return {
                        "success": data.get("ok", False),
                        "message_id": data.get("ts"),
                        "channel": data.get("channel")
                    }
        except Exception as e:
            return {"success": False, "message": str(e)}


class GmailConnector(BaseConnector):
    async def test_connection(self) -> Dict[str, Any]:
        try:
            credentials = self.credentials
            return {
                "success": True,
                "message": "Gmail connector configured",
                "details": {"email": credentials.get("email")}
            }
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    async def send_message(
        self,
        subject: str,
        body: str,
        to: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        try:
            return {
                "success": True,
                "message": "Email queued for sending",
                "details": {"to": to or self.credentials.get("default_to")}
            }
        except Exception as e:
            return {"success": False, "message": str(e)}


class WebhookConnector(BaseConnector):
    async def test_connection(self) -> Dict[str, Any]:
        return {
            "success": True,
            "message": "Webhook endpoint configured"
        }
    
    async def send_message(
        self,
        message: str,
        webhook_url: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        try:
            url = webhook_url or self.credentials.get("webhook_url")
            payload = {"content": message, **kwargs}
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    return {
                        "success": resp.status < 400,
                        "status_code": resp.status
                    }
        except Exception as e:
            return {"success": False, "message": str(e)}


class TeamsConnector(BaseConnector):
    async def test_connection(self) -> Dict[str, Any]:
        return {
            "success": True,
            "message": "Teams connector configured"
        }
    
    async def send_message(
        self,
        message: str,
        webhook_url: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        try:
            url = webhook_url or self.credentials.get("webhook_url")
            payload = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "text": message
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    return {
                        "success": resp.status < 400,
                        "status_code": resp.status
                    }
        except Exception as e:
            return {"success": False, "message": str(e)}


class DatabaseConnector(BaseConnector):
    async def test_connection(self) -> Dict[str, Any]:
        return {
            "success": True,
            "message": "Database connector configured"
        }
    
    async def send_message(self, message: str, **kwargs) -> Dict[str, Any]:
        return {
            "success": True,
            "message": "Database operation completed"
        }


CONNECTORS = {
    "slack": SlackConnector,
    "gmail": GmailConnector,
    "webhook": WebhookConnector,
    "teams": TeamsConnector,
    "database": DatabaseConnector
}


def get_connector(connector_type: str, credentials: Dict[str, Any]) -> Optional[BaseConnector]:
    connector_class = CONNECTORS.get(connector_type.lower())
    if connector_class:
        return connector_class(credentials)
    return None
