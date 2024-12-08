from bigbytes.orchestration.triggers.loop_time_trigger import LoopTimeTrigger
from bigbytes.tests.base_test import TestCase
from unittest.mock import patch


class LoopTimeTriggerTests(TestCase):
    @patch('bigbytes.orchestration.triggers.time_trigger.check_sla')
    @patch('bigbytes.orchestration.triggers.time_trigger.schedule_all')
    def test_run(self, mock_schedule_all, mock_check_sla):
        trigger = LoopTimeTrigger()
        trigger.run()
        mock_schedule_all.assert_called_once()
        mock_check_sla.assert_called_once()
