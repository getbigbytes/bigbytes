from typing import Dict

from bigbytes.api.constants import AuthorizeStatusType
from bigbytes.api.oauth_scope import OauthScopeType
from bigbytes.api.operations.constants import OperationType
from bigbytes.api.parsers.BaseParser import BaseParser
from bigbytes.api.presenters.RolePresenter import RolePresenter
from bigbytes.shared.hash import extract


class RoleParser(BaseParser):
    pass


async def parse_read(parser, value: Dict, **kwargs) -> Dict:
    return extract(value, RolePresenter.default_attributes)


RoleParser.parse_read(
    parser=parse_read,
    on_action=[
        OperationType.DETAIL,
    ],
    on_authorize_status=[
        AuthorizeStatusType.FAILED,
    ],
    scopes=[
        OauthScopeType.CLIENT_PRIVATE,
    ],
)
