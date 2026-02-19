"""LLM provider adapters for runtime step generation."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class LLMProviderError(RuntimeError):
    """Raised when LLM generation fails."""


@dataclass
class LLMConfig:
    provider: str
    model: str
    api_key: str
    base_url: Optional[str] = None
    timeout_seconds: int = 30
    base_prompt: Optional[str] = None


class LLMClient:
    """Minimal REST client for supported LLM providers."""

    def __init__(self, config: LLMConfig) -> None:
        self.config = config

    @classmethod
    def from_env(
        cls,
        provider: str,
        model: str,
        api_key_env: str,
        base_url: str | None = None,
        base_prompt_file: str | None = None,
    ) -> "LLMClient":
        api_key = os.getenv(api_key_env, "")
        if not api_key:
            raise LLMProviderError(
                f"missing API key in environment variable `{api_key_env}`"
            )

        prompt = None
        if base_prompt_file:
            prompt = Path(base_prompt_file).read_text(encoding="utf-8")

        return cls(
            LLMConfig(
                provider=provider,
                model=model,
                api_key=api_key,
                base_url=base_url,
                base_prompt=prompt,
            )
        )

    def generate_assistant_text(
        self,
        *,
        phase: str,
        mode: str,
        user_input: str,
        project_id: str,
        context_bundle: Dict[str, Any] | None = None,
    ) -> str:
        system_prompt = self._compose_system_prompt()
        user_prompt = self._compose_user_prompt(
            phase=phase,
            mode=mode,
            user_input=user_input,
            project_id=project_id,
            context_bundle=context_bundle or {},
        )

        provider = self.config.provider.lower()
        if provider == "openai":
            return self._call_openai(system_prompt, user_prompt)
        if provider == "anthropic":
            return self._call_anthropic(system_prompt, user_prompt)
        raise LLMProviderError(f"unsupported provider `{self.config.provider}`")

    def _compose_system_prompt(self) -> str:
        base = self.config.base_prompt or (
            "You are SPECULA AI. Output must start with `MODE: <mode> | PHASE: <phase>`, "
            "include max 6 lines before one single question, and avoid prescriptive language."
        )
        return base

    @staticmethod
    def _compose_user_prompt(
        *,
        phase: str,
        mode: str,
        user_input: str,
        project_id: str,
        context_bundle: Dict[str, Any],
    ) -> str:
        context_json = json.dumps(context_bundle, ensure_ascii=True)
        return (
            "Generate only the assistant text for one Specula turn.\n"
            f"Project ID: {project_id}\n"
            f"Target phase: {phase}\n"
            f"Target mode: {mode}\n"
            f"Continuity context: {context_json}\n"
            f"Latest user input: {user_input}\n"
            "Constraints: one question only, no recommendations, no rankings, no decision language."
        )

    def _call_openai(self, system_prompt: str, user_prompt: str) -> str:
        endpoint = self.config.base_url or "https://api.openai.com/v1/chat/completions"
        payload = {
            "model": self.config.model,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        response = self._post_json(endpoint, payload, headers)
        try:
            content = response["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMProviderError("invalid OpenAI response format") from exc
        if not isinstance(content, str) or not content.strip():
            raise LLMProviderError("empty OpenAI assistant content")
        return content.strip()

    def _call_anthropic(self, system_prompt: str, user_prompt: str) -> str:
        endpoint = self.config.base_url or "https://api.anthropic.com/v1/messages"
        payload = {
            "model": self.config.model,
            "max_tokens": 400,
            "temperature": 0.2,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": user_prompt}],
                }
            ],
        }
        headers = {
            "x-api-key": self.config.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        response = self._post_json(endpoint, payload, headers)
        try:
            blocks = response["content"]
            content = "\n".join(
                block.get("text", "")
                for block in blocks
                if isinstance(block, dict) and block.get("type") == "text"
            )
        except (KeyError, TypeError) as exc:
            raise LLMProviderError("invalid Anthropic response format") from exc

        if not content.strip():
            raise LLMProviderError("empty Anthropic assistant content")
        return content.strip()

    def _post_json(self, url: str, payload: dict, headers: dict) -> dict:
        request = Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.config.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
        except HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
            raise LLMProviderError(f"provider HTTP error {exc.code}: {details}") from exc
        except URLError as exc:
            raise LLMProviderError(f"provider connection error: {exc.reason}") from exc

        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LLMProviderError("provider returned non-JSON response") from exc
