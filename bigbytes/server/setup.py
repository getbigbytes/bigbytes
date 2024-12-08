from bigbytes.settings.server import KERNEL_MAGIC


def initialize_globals():
    from bigbytes.orchestration.job_manager import get_job_manager

    print('Initializing global job manager: ', get_job_manager())

    if KERNEL_MAGIC:
        from bigbytes.kernels.magic.queues.manager import get_execution_result_queue

        print('Initializing global execution result queue: ', get_execution_result_queue())
