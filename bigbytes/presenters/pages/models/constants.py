from bigbytes.shared.enum import StrEnum


class ComponentCategory(StrEnum):
    BUTTON = 'button'
    FIELD = 'field'
    FORM = 'form'


class PageCategory(StrEnum):
    COMMUNITY = 'community'


class ResourceType(StrEnum):
    PIPELINE = 'pipeline'
    PIPELINE_SCHEDULE = 'pipeline_schedule'
