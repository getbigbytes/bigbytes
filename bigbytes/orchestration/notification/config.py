from dataclasses import dataclass, field
from typing import List

from bigbytes.services.discord.config import DiscordConfig
from bigbytes.services.email.config import EmailConfig
from bigbytes.services.google_chat.config import GoogleChatConfig
from bigbytes.services.opsgenie.config import OpsgenieConfig
from bigbytes.services.slack.config import SlackConfig
from bigbytes.services.teams.config import TeamsConfig
from bigbytes.services.telegram.config import TelegramConfig
from bigbytes.shared.config import BaseConfig
from bigbytes.shared.enum import StrEnum


class AlertOn(StrEnum):
    PIPELINE_RUN_FAILURE = 'trigger_failure'
    PIPELINE_RUN_SUCCESS = 'trigger_success'
    PIPELINE_RUN_PASSED_SLA = 'trigger_passed_sla'


DEFAULT_ALERT_ON = [
    AlertOn.PIPELINE_RUN_FAILURE,
    AlertOn.PIPELINE_RUN_PASSED_SLA,
]


@dataclass
class MessageTemplate(BaseConfig):
    title: str = None
    summary: str = None
    details: str = None


@dataclass
class MessageTemplates(BaseConfig):
    success: MessageTemplate = None
    failure: MessageTemplate = None
    passed_sla: MessageTemplate = None


@dataclass
class NotificationConfig(BaseConfig):
    alert_on: List[AlertOn] = field(default_factory=lambda: DEFAULT_ALERT_ON)
    email_config: EmailConfig = None
    google_chat_config: GoogleChatConfig = None
    opsgenie_config: OpsgenieConfig = None
    slack_config: SlackConfig = None
    teams_config: TeamsConfig = None
    discord_config: DiscordConfig = None
    telegram_config: TelegramConfig = None
    message_templates: MessageTemplates = None
