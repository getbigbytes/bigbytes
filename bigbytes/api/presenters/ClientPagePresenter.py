from bigbytes.api.operations import constants
from bigbytes.api.presenters.BasePresenter import BasePresenter


class ClientPagePresenter(BasePresenter):
    default_attributes = [
        'category',
        'disabled',
        'enabled',
        'operation',
        'parent',
        'resource',
        'uuid',
        'version',
    ]

    async def prepare_present(self, **kwargs):
        return await self.model.to_dict(
            current_user=self.current_user,
            **(self.resource.result_set().context.data.get('resources') or {}),
        )


ClientPagePresenter.register_format(
    constants.DETAIL,
    ClientPagePresenter.default_attributes + [
        'components',
        'metadata',
    ],
)
