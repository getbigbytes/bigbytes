from unittest.mock import patch

from faker import Faker

from bigbytes.data_preparation.models.block.hook.block import HookBlock
from bigbytes.data_preparation.models.constants import BlockType
from bigbytes.data_preparation.models.global_hooks.models import HookStatus, HookStrategy
from bigbytes.shared.constants import ENV_TEST_BIGBYTES
from bigbytes.tests.api.operations.test_base import BaseApiTestCase
from bigbytes.tests.factory import create_pipeline_with_blocks
from bigbytes.tests.shared.mixins import build_hooks


class HookBlockTest(BaseApiTestCase):
    def setUp(self):
        self.faker = Faker()

        self.pipeline1 = create_pipeline_with_blocks(
            self.faker.unique.name(),
            self.repo_path,
        )

        _global_hooks, _hooks, hooks_match, _hooks_miss = build_hooks(self, self.pipeline1)

        self.hooks = hooks_match
        self.hook = hooks_match[0]

    def tearDown(self):
        self.pipeline1.delete()
        super().tearDown()

    def test_execute_block(self):
        block = HookBlock(
            self.hook.uuid,
            self.hook.uuid,
            BlockType.HOOK,
            hook=self.hook,
        )
        global_vars = dict(bigbytes=1)

        with patch.object(block.hook, 'run') as mock_run:
            block.execute_sync(global_vars=global_vars)

            mock_run.assert_called_once_with(
                block_uuid=block.uuid,
                check_status=True,
                configuration={},
                context={},
                env=ENV_TEST_BIGBYTES,
                error_on_failure=True,
                bigbytes=1,
                pipeline_uuid='',
                poll_interval=10,
                strategies=[HookStrategy.RAISE],
                with_trigger=True,
            )

    def test_execute_block_with_error(self):
        self.hook.strategies = [HookStrategy.CONTINUE]
        self.hook.pipeline_settings = dict(
            uuid=self.pipeline1.uuid,
        )

        block = HookBlock(
            self.hook.uuid,
            self.hook.uuid,
            BlockType.HOOK,
            hook=self.hook,
        )
        global_vars = dict(bigbytes=1)

        self.hook.status = HookStatus.load(error=Exception('bigbytes'), strategy=HookStrategy.RAISE)

        with patch.object(block.hook, 'run') as mock_run:
            error = None
            try:
                block.execute_sync(global_vars=global_vars)
            except Exception as err:
                error = err

            self.assertEqual(str(error), 'bigbytes')

            mock_run.assert_called_once_with(
                block_uuid=block.uuid,
                check_status=True,
                configuration={},
                context={},
                env=ENV_TEST_BIGBYTES,
                error_on_failure=True,
                bigbytes=1,
                pipeline_uuid='',
                poll_interval=10,
                strategies=[HookStrategy.RAISE],
                with_trigger=True,
            )

            self.hook.status = HookStatus.load(
                error=Exception('bigbytes'),
                strategy=HookStrategy.CONTINUE,
            )
            self.assertEqual(block.execute_sync(global_vars=global_vars)['output'], ['bigbytes'])
