import os
from pathlib import Path
from urllib.parse import quote_plus, urlparse

from arq.connections import RedisSettings
from codex_platform.workers.arq import BaseWorkerConfig
from pydantic import Field
from pydantic_settings import SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_FILE_PATH = ROOT_DIR / ".env"


class WorkerSettings(BaseWorkerConfig):
    """Runtime settings shared by standalone ARQ workers."""

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    project_name: str = Field(default="atlas", alias="PROJECT_NAME")
    redis_url_env: str | None = Field(default=None, alias="REDIS_URL")
    arq_redis_url_env: str | None = Field(default=None, alias="ARQ_REDIS_URL")

    upstash_redis_rest_url: str | None = Field(default=None, alias="UPSTASH_REDIS_REST_URL")
    upstash_redis_host: str | None = Field(default=None, alias="UPSTASH_REDIS_HOST")
    upstash_redis_password: str | None = Field(default=None, alias="UPSTASH_REDIS_PASSWORD")

    ai_provider: str = Field(default="gemini", alias="AI_PROVIDER")
    ai_model: str = Field(default="gemini-2.5-flash", alias="AI_MODEL")
    gemini_api_key: str | None = Field(default=None, alias="GEMINI_API_KEY")
    google_api_key: str | None = Field(default=None, alias="GOOGLE_API_KEY")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")
    ai_max_retries: int = Field(default=2, alias="AI_MAX_RETRIES")
    ai_retry_delay_seconds: float = Field(default=2.0, alias="AI_RETRY_DELAY_SECONDS")
    ai_stub_when_unconfigured: bool = Field(default=True, alias="AI_STUB_WHEN_UNCONFIGURED")

    smtp_from_name: str = Field(default="Atlas", alias="EMAIL_FROM_NAME")

    log_level_console: str = "INFO"
    log_level_file: str = "DEBUG"
    log_rotation: str = "10 MB"
    log_dir_name: str = "logs"

    @property
    def is_inside_docker(self) -> bool:
        return os.environ.get("IS_DOCKER", "False").lower() in ("true", "1", "t") or os.path.exists("/.dockerenv")

    @property
    def effective_redis_host(self) -> str:
        return "redis" if self.redis_host == "localhost" and self.is_inside_docker else self.redis_host

    @property
    def log_dir(self) -> str:
        return str(ROOT_DIR / self.log_dir_name)

    @log_dir.setter
    def log_dir(self, value: str) -> None:
        pass

    @property
    def service_name_suffix(self) -> str:
        return "" if self.is_inside_docker else "_local"

    @property
    def log_file_debug(self) -> str:
        service_name = f"{self.project_name}{self.service_name_suffix}"
        return f"{self.log_dir}/{service_name}/debug.log"

    @property
    def log_file_errors(self) -> str:
        service_name = f"{self.project_name}{self.service_name_suffix}"
        return f"{self.log_dir}/{service_name}/errors.json"

    @property
    def redis_url(self) -> str:
        if self.arq_redis_url_env:
            return self.arq_redis_url_env
        if self.redis_url_env:
            return self.redis_url_env
        if self.upstash_redis_password:
            host = self.upstash_redis_host or ""
            if not host and self.upstash_redis_rest_url:
                host = urlparse(self.upstash_redis_rest_url).hostname or ""
            if host:
                password = quote_plus(self.upstash_redis_password.strip("'\"").strip())
                return f"rediss://default:{password}@{host}:6379/0"
        return super().redis_url.replace(self.redis_host, self.effective_redis_host, 1)

    @property
    def arq_redis_settings(self) -> RedisSettings:
        return RedisSettings.from_dsn(self.redis_url)
