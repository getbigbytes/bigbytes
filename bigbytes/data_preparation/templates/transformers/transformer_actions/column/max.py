from bigbytes.data_cleaner.transformer_actions.base import BaseAction
from bigbytes.data_cleaner.transformer_actions.constants import ActionType, Axis
from bigbytes.data_cleaner.transformer_actions.utils import build_transformer_action
from pandas import DataFrame

if 'transformer' not in globals():
    from bigbytes.data_preparation.decorators import transformer


@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Execute Transformer Action: ActionType.MAX

    Docs: https://docs.bigbytes.io/guides/transformer-blocks#aggregation-actions
    """
    action = build_transformer_action(
        df,
        action_type=ActionType.MAX,
        action_code='',  # Enter filtering condition on rows before aggregation
        arguments=[],  # Enter the columns to compute aggregate over
        axis=Axis.COLUMN,
        options={'groupby_columns': []},  # Enter columns to group by
        outputs=[
            # The number of outputs below must match the number of arguments
            {'uuid': 'new_aggregate_column', 'column_type': 'number_with_decimals'},
        ],
    )

    return BaseAction(action).execute(df)
