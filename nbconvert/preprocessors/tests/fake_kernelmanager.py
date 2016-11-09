from jupyter_client.manager import KernelManager


class FakeCustomKernelManager(KernelManager):
    expected_methods = {
        '__init__': 0,
        'start_kernel': 0
    }

    def __init__(self, *args, **kwargs):
        self.log.info('FakeCustomKernelManager initialized')
        self.expected_methods['__init__'] += 1
        super(FakeCustomKernelManager, self).__init__(*args, **kwargs)

    def start_kernel(self, *args, **kwargs):
        self.log.info('FakeCustomKernelManager started a kernel')
        self.expected_methods['start_kernel'] += 1
        return super(FakeCustomKernelManager, self).start_kernel(
            *args,
            **kwargs)
