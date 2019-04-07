# coding=utf-8

"""
Module with tests for the execute preprocessor.
"""

# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from base64 import b64encode, b64decode
import copy
import glob
import io
import os
import re

import nbformat
import sys
import pytest
import functools

from .base import PreprocessorTestsBase
from ..execute import ExecutePreprocessor, CellExecutionError, executenb

import IPython
from mock import patch, MagicMock
from traitlets import TraitError
from jupyter_client.kernelspec import KernelSpecManager
from nbconvert.filters import strip_ansi
from testpath import modified_env
from ipython_genutils.py3compat import string_types

try:
    TimeoutError  # Py 3
except NameError:
    TimeoutError = RuntimeError  # Py 2

addr_pat = re.compile(r'0x[0-9a-f]{7,9}')
ipython_input_pat = re.compile(r'<ipython-input-\d+-[0-9a-f]+>')
current_dir = os.path.dirname(__file__)

def _normalize_base64(b64_text):
    # if it's base64, pass it through b64 decode/encode to avoid
    # equivalent values from being considered unequal
    try:
        return b64encode(b64decode(b64_text.encode('ascii'))).decode('ascii')
    except (ValueError, TypeError):
        return b64_text


def merge_dicts(first, second):
    # Because this is annoying to do inline
    outcome = {}
    outcome.update(first)
    outcome.update(second)
    return outcome


class ExecuteTestBase(PreprocessorTestsBase):
    def build_preprocessor(self, opts):
        """Make an instance of a preprocessor"""
        preprocessor = ExecutePreprocessor()
        preprocessor.enabled = True
        for opt in opts:
            setattr(preprocessor, opt, opts[opt])
        # Perform some state setup that should probably be in the init
        preprocessor._display_id_map = {}
        preprocessor.widget_state = {}
        preprocessor.widget_buffers = {}
        return preprocessor

    @staticmethod
    def prepare_cell_mocks(*messages):
        messages = list(messages)
        def prepared_wrapper(func):
            @functools.wraps(func)
            def test_mock_wrapper(self):
                parent_id = 'fake_id'
                cell_mock = MagicMock(source='"foo" = "bar"', outputs=[])
                # Hack to help catch `.` and `[]` style access to outputs against the same mock object
                cell_mock.__getitem__.side_effect = lambda n: cell_mock.outputs if n == 'outputs' else None
                preprocessor = self.build_preprocessor({})
                preprocessor.nb = {'cells': [cell_mock]}
                shell_message_mock = MagicMock(
                    return_value={'parent_header': {'msg_id': parent_id}})
                # Always terminate messages with an idle to exit the loop
                messages.append({'msg_type': 'status', 'content': {'execution_state': 'idle'}})
                message_mock = MagicMock(
                    side_effect=[
                        # Default the parent_header so mocks don't need to include this
                        merge_dicts({'parent_header': {'msg_id': parent_id}}, msg)
                        for msg in messages
                    ]
                )
                channel_mock = MagicMock(get_msg=message_mock)
                shell_mock = MagicMock(get_msg=shell_message_mock)
                preprocessor.kc = MagicMock(
                    iopub_channel=channel_mock,
                    shell_channel=shell_mock,
                    execute=MagicMock(return_value=parent_id)
                )
                return func(self, preprocessor, cell_mock, message_mock)
            return test_mock_wrapper
        return prepared_wrapper


class TestExecute(ExecuteTestBase):
    """Contains test functions for execute.py"""
    maxDiff = None

    @staticmethod
    def normalize_output(output):
        """
        Normalizes outputs for comparison.
        """
        output = dict(output)
        if 'metadata' in output:
            del output['metadata']
        if 'text' in output:
            output['text'] = re.sub(addr_pat, '<HEXADDR>', output['text'])
        if 'text/plain' in output.get('data', {}):
            output['data']['text/plain'] = \
                re.sub(addr_pat, '<HEXADDR>', output['data']['text/plain'])
        if 'application/vnd.jupyter.widget-view+json' in output.get('data', {}):
            output['data']['application/vnd.jupyter.widget-view+json'] \
                ['model_id'] = '<MODEL_ID>'
        for key, value in output.get('data', {}).items():
            if isinstance(value, string_types):
                if sys.version_info.major == 2:
                    value = value.replace('u\'', '\'')
                output['data'][key] = _normalize_base64(value)
        if 'traceback' in output:
            tb = [
                re.sub(ipython_input_pat, '<IPY-INPUT>', strip_ansi(line))
                for line in output['traceback']
            ]
            output['traceback'] = tb

        return output


    def assert_notebooks_equal(self, expected, actual):
        expected_cells = expected['cells']
        actual_cells = actual['cells']
        self.assertEqual(len(expected_cells), len(actual_cells))

        for expected_cell, actual_cell in zip(expected_cells, actual_cells):
            expected_outputs = expected_cell.get('outputs', [])
            actual_outputs = actual_cell.get('outputs', [])
            normalized_expected_outputs = list(map(self.normalize_output, expected_outputs))
            normalized_actual_outputs = list(map(self.normalize_output, actual_outputs))
            self.assertEqual(normalized_expected_outputs, normalized_actual_outputs)

            expected_execution_count = expected_cell.get('execution_count', None)
            actual_execution_count = actual_cell.get('execution_count', None)
            self.assertEqual(expected_execution_count, actual_execution_count)


    def test_constructor(self):
        """Can a ExecutePreprocessor be constructed?"""
        self.build_preprocessor({})


    def run_notebook(self, filename, opts, resources):
        """Loads and runs a notebook, returning both the version prior to
        running it and the version after running it.

        """
        with io.open(filename) as f:
            input_nb = nbformat.read(f, 4)

        preprocessor = self.build_preprocessor(opts)
        cleaned_input_nb = copy.deepcopy(input_nb)
        for cell in cleaned_input_nb.cells:
            if 'execution_count' in cell:
                del cell['execution_count']
            cell['outputs'] = []

        # Override terminal size to standardise traceback format
        with modified_env({'COLUMNS': '80', 'LINES': '24'}):
            output_nb, _ = preprocessor(cleaned_input_nb, resources)

        return input_nb, output_nb

    def test_run_notebooks(self):
        """Runs a series of test notebooks and compares them to their actual output"""
        input_files = glob.glob(os.path.join(current_dir, 'files', '*.ipynb'))
        shared_opts = dict(kernel_name="python")
        for filename in input_files:
            # There is some slight differences between the output in IPython 6 and IPython 7.
            IPY_MAJOR = IPython.version_info[0]
            if os.path.basename(filename).endswith("-IPY6.ipynb"):
                print(filename, IPY_MAJOR)
                if IPY_MAJOR >= 7:
                    continue
            elif os.path.basename(filename) in ("Interrupt.ipynb", "Skip Exceptions with Cell Tags.ipynb", "Skip Exceptions.ipynb"):
                if IPY_MAJOR < 7:
                    continue

            # Special arguments for the notebooks
            if os.path.basename(filename) == "Disable Stdin.ipynb":
                continue
            elif os.path.basename(filename) in ("Interrupt.ipynb", "Interrupt-IPY6.ipynb"):
                opts = dict(timeout=1, interrupt_on_timeout=True, allow_errors=True)
            elif os.path.basename(filename) in ("Skip Exceptions.ipynb", "Skip Exceptions-IPY6.ipynb"):
                opts = dict(allow_errors=True)
            else:
                opts = dict()
            res = self.build_resources()
            res['metadata']['path'] = os.path.dirname(filename)
            opts.update(shared_opts)
            input_nb, output_nb = self.run_notebook(filename, opts, res)
            self.assert_notebooks_equal(input_nb, output_nb)

    def test_populate_language_info(self):
        preprocessor = self.build_preprocessor(opts=dict(kernel_name="python"))
        nb = nbformat.v4.new_notebook()  # Certainly has no language_info.
        nb, _ = preprocessor.preprocess(nb, resources={})
        assert 'language_info' in nb.metadata

    def test_empty_path(self):
        """Can the kernel be started when the path is empty?"""
        filename = os.path.join(current_dir, 'files', 'HelloWorld.ipynb')
        res = self.build_resources()
        res['metadata']['path'] = ''
        input_nb, output_nb = self.run_notebook(filename, {}, res)
        self.assert_notebooks_equal(input_nb, output_nb)

    @pytest.mark.xfail("python3" not in KernelSpecManager().find_kernel_specs(),
                        reason="requires a python3 kernelspec")
    def test_empty_kernel_name(self):
        """Can kernel in nb metadata be found when an empty string is passed?

        Note: this pattern should be discouraged in practice.
        Passing in no kernel_name to ExecutePreprocessor is recommended instead.
        """
        filename = os.path.join(current_dir, 'files', 'UnicodePy3.ipynb')
        res = self.build_resources()
        input_nb, output_nb = self.run_notebook(filename, {"kernel_name": ""}, res)
        self.assert_notebooks_equal(input_nb, output_nb)
        with pytest.raises(TraitError):
            input_nb, output_nb = self.run_notebook(filename, {"kernel_name": None}, res)

    def test_disable_stdin(self):
        """Test disabling standard input"""
        filename = os.path.join(current_dir, 'files', 'Disable Stdin.ipynb')
        res = self.build_resources()
        res['metadata']['path'] = os.path.dirname(filename)
        input_nb, output_nb = self.run_notebook(filename, dict(allow_errors=True), res)

        # We need to special-case this particular notebook, because the
        # traceback contains machine-specific stuff like where IPython
        # is installed. It is sufficient here to just check that an error
        # was thrown, and that it was a StdinNotImplementedError
        self.assertEqual(len(output_nb['cells']), 1)
        self.assertEqual(len(output_nb['cells'][0]['outputs']), 1)
        output = output_nb['cells'][0]['outputs'][0]
        self.assertEqual(output['output_type'], 'error')
        self.assertEqual(output['ename'], 'StdinNotImplementedError')
        self.assertEqual(output['evalue'], 'raw_input was called, but this frontend does not support input requests.')

    def test_timeout(self):
        """Check that an error is raised when a computation times out"""
        filename = os.path.join(current_dir, 'files', 'Interrupt.ipynb')
        res = self.build_resources()
        res['metadata']['path'] = os.path.dirname(filename)

        with pytest.raises(TimeoutError):
            self.run_notebook(filename, dict(timeout=1), res)

    def test_timeout_func(self):
        """Check that an error is raised when a computation times out"""
        filename = os.path.join(current_dir, 'files', 'Interrupt.ipynb')
        res = self.build_resources()
        res['metadata']['path'] = os.path.dirname(filename)

        def timeout_func(source):
            return 10

        with pytest.raises(TimeoutError):
            self.run_notebook(filename, dict(timeout_func=timeout_func), res)

    @patch('jupyter_client.KernelManager.is_alive')
    def test_kernel_death(self, alive_mock):
        """Check that an error is raised when the kernel is_alive is false"""
        current_dir = os.path.dirname(__file__)
        filename = os.path.join(current_dir, 'files', 'Interrupt.ipynb')
        res = self.build_resources()
        res['metadata']['path'] = os.path.dirname(filename)

        with pytest.raises(RuntimeError):
            alive_mock.return_value = False
            self.run_notebook(filename, {}, res)

    def test_allow_errors(self):
        """
        Check that conversion halts if ``allow_errors`` is False.
        """
        filename = os.path.join(current_dir, 'files', 'Skip Exceptions.ipynb')
        res = self.build_resources()
        res['metadata']['path'] = os.path.dirname(filename)
        with pytest.raises(CellExecutionError) as exc:
            self.run_notebook(filename, dict(allow_errors=False), res)
            self.assertIsInstance(str(exc.value), str)
            if sys.version_info >= (3, 0):
                assert u"# üñîçø∂é" in str(exc.value)
            else:
                assert u"# üñîçø∂é".encode('utf8', 'replace') in str(exc.value)

    def test_force_raise_errors(self):
        """
        Check that conversion halts if the ``force_raise_errors`` traitlet on
        ExecutePreprocessor is set to True.
        """
        filename = os.path.join(current_dir, 'files',
                                'Skip Exceptions with Cell Tags.ipynb')
        res = self.build_resources()
        res['metadata']['path'] = os.path.dirname(filename)
        with pytest.raises(CellExecutionError) as exc:
            self.run_notebook(filename, dict(force_raise_errors=True), res)
            self.assertIsInstance(str(exc.value), str)
            if sys.version_info >= (3, 0):
                assert u"# üñîçø∂é" in str(exc.value)
            else:
                assert u"# üñîçø∂é".encode('utf8', 'replace') in str(exc.value)

    def test_custom_kernel_manager(self):
        from .fake_kernelmanager import FakeCustomKernelManager

        filename = os.path.join(current_dir, 'files', 'HelloWorld.ipynb')

        with io.open(filename) as f:
            input_nb = nbformat.read(f, 4)

        preprocessor = self.build_preprocessor({
            'kernel_manager_class': FakeCustomKernelManager
        })

        cleaned_input_nb = copy.deepcopy(input_nb)
        for cell in cleaned_input_nb.cells:
            if 'execution_count' in cell:
                del cell['execution_count']
            cell['outputs'] = []

        # Override terminal size to standardise traceback format
        with modified_env({'COLUMNS': '80', 'LINES': '24'}):
            output_nb, _ = preprocessor(cleaned_input_nb,
                                        self.build_resources())

        expected = FakeCustomKernelManager.expected_methods.items()

        for method, call_count in expected:
            self.assertNotEqual(call_count, 0, '{} was called'.format(method))

    def test_execute_function(self):
        # Test the executenb() convenience API
        filename = os.path.join(current_dir, 'files', 'HelloWorld.ipynb')

        with io.open(filename) as f:
            input_nb = nbformat.read(f, 4)

        original = copy.deepcopy(input_nb)
        executed = executenb(original, os.path.dirname(filename))
        self.assert_notebooks_equal(original, executed)

    def test_widgets(self):
        """Runs a test notebook with widgets and checks the widget state is saved."""
        input_file = os.path.join(current_dir, 'files', 'JupyterWidgets.ipynb')
        opts = dict(kernel_name="python")
        res = self.build_resources()
        res['metadata']['path'] = os.path.dirname(input_file)
        input_nb, output_nb = self.run_notebook(input_file, opts, res)

        output_data = [
            output.get('data', {})
            for cell in output_nb['cells']
            for output in cell['outputs']
        ]

        model_ids = [
            data['application/vnd.jupyter.widget-view+json']['model_id']
            for data in output_data
            if 'application/vnd.jupyter.widget-view+json' in data
        ]

        wdata = output_nb['metadata']['widgets'] \
                ['application/vnd.jupyter.widget-state+json']
        for k in model_ids:
            d = wdata['state'][k]
            assert 'model_name' in d
            assert 'model_module' in d
            assert 'state' in d
        assert 'version_major' in wdata
        assert 'version_minor' in wdata


class TestRunCell(ExecuteTestBase):
    """Contains test functions for ExecutePreprocessor.run_cell"""

    @ExecuteTestBase.prepare_cell_mocks()
    def test_idle_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # Just the exit message should be fetched
        message_mock.assert_called_once()
        # Ensure no outputs were generated
        self.assertFalse(cell_mock.outputs)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'stream',
        'header': {'msg_type': 'execute_reply'},
        'parent_header': {'msg_id': 'wrong_parent'},
        'content': {'name': 'stdout', 'text': 'foo'}
    })
    def test_message_for_wrong_parent(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # An ignored stream followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        # Ensure no output was written
        self.assertFalse(cell_mock.outputs)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'status',
        'header': {'msg_type': 'status'},
        'content': {'execution_state': 'busy'}
    })
    def test_busy_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # One busy message, followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        # Ensure no outputs were generated
        self.assertFalse(cell_mock.outputs)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'execute_input',
        'header': {'msg_type': 'execute_input'},
        'content': {}
    })
    def test_execute_input_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # One ignored execute_input, followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        # Ensure no outputs were generated
        self.assertFalse(cell_mock.outputs)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'stream',
        'header': {'msg_type': 'stream'},
        'content': {'name': 'stdout', 'text': 'foo'},
    }, {
        'msg_type': 'stream',
        'header': {'msg_type': 'stream'},
        'content': {'name': 'stderr', 'text': 'bar'}
    })
    def test_stream_messages(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # An stdout then stderr stream followed by an idle
        self.assertEqual(message_mock.call_count, 3)
        # Ensure the output was captured
        self.assertListEqual(cell_mock.outputs, [
            {'output_type': 'stream', 'name': 'stdout', 'text': 'foo'},
            {'output_type': 'stream', 'name': 'stderr', 'text': 'bar'}
        ])

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'stream',
        'header': {'msg_type': 'execute_reply'},
        'content': {'name': 'stdout', 'text': 'foo'}
    }, {
        'msg_type': 'clear_output',
        'header': {'msg_type': 'clear_output'},
        'content': {}
    })
    def test_clear_output_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # A stream, followed by a clear, and then an idle
        self.assertEqual(message_mock.call_count, 3)
        # Ensure the output was cleared
        self.assertFalse(cell_mock.outputs)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'stream',
        'header': {'msg_type': 'stream'},
        'content': {'name': 'stdout', 'text': 'foo'}
    }, {
        'msg_type': 'clear_output',
        'header': {'msg_type': 'clear_output'},
        'content': {'wait': True}
    })
    def test_clear_output_wait_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # A stream, followed by a clear, and then an idle
        self.assertEqual(message_mock.call_count, 3)
        # Should be true without another message to trigger the clear
        self.assertTrue(preprocessor.clear_before_next_output)
        # Ensure the output wasn't cleared yet
        self.assertListEqual(cell_mock.outputs, [
            {'output_type': 'stream', 'name': 'stdout', 'text': 'foo'}
        ])

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'stream',
        'header': {'msg_type': 'stream'},
        'content': {'name': 'stdout', 'text': 'foo'}
    }, {
        'msg_type': 'clear_output',
        'header': {'msg_type': 'clear_output'},
        'content': {'wait': True}
    }, {
        'msg_type': 'stream',
        'header': {'msg_type': 'stream'},
        'content': {'name': 'stderr', 'text': 'bar'}
    })
    def test_clear_output_wait_then_message_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # An stdout stream, followed by a wait clear, an stderr stream, and then an idle
        self.assertEqual(message_mock.call_count, 4)
        # Should be false after the stderr message
        self.assertFalse(preprocessor.clear_before_next_output)
        # Ensure the output wasn't cleared yet
        self.assertListEqual(cell_mock.outputs, [
            {'output_type': 'stream', 'name': 'stderr', 'text': 'bar'}
        ])

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'execute_reply',
        'header': {'msg_type': 'execute_reply'},
        'content': {'execution_count': 42}
    })
    def test_execution_count_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # An execution count followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        cell_mock.__setitem__.assert_called_once_with('execution_count', 42)
        # Ensure no outputs were generated
        self.assertFalse(cell_mock.outputs)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'stream',
        'header': {'msg_type': 'stream'},
        'content': {'execution_count': 42, 'name': 'stdout', 'text': 'foo'}
    })
    def test_execution_count_with_stream_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # An execution count followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        cell_mock.__setitem__.assert_called_once_with('execution_count', 42)
        # Should also consume the message stream
        self.assertListEqual(cell_mock.outputs, [
            {'output_type': 'stream', 'name': 'stdout', 'text': 'foo'}
        ])

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'comm',
        'header': {'msg_type': 'comm'},
        'content': {
            'comm_id': 'foobar',
            'data': {'state': {'foo': 'bar'}}
        }
    })
    def test_widget_comm_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # A comm message without buffer info followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        self.assertEqual(preprocessor.widget_state, {'foobar': {'foo': 'bar'}})
        # Buffers should still be empty
        self.assertFalse(preprocessor.widget_buffers)
        # Ensure no outputs were generated
        self.assertFalse(cell_mock.outputs)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'comm',
        'header': {'msg_type': 'comm'},
        'buffers': [b'123'],
        'content': {
            'comm_id': 'foobar',
            'data': {
                'state': {'foo': 'bar'},
                'buffer_paths': ['path']
            }
        }
    })
    def test_widget_comm_buffer_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # A comm message with buffer info followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        self.assertEqual(preprocessor.widget_state, {'foobar': {'foo': 'bar'}})
        self.assertEqual(preprocessor.widget_buffers,
            {'foobar': [{'data': 'MTIz', 'encoding': 'base64', 'path': 'path'}]}
        )
        # Ensure no outputs were generated
        self.assertFalse(cell_mock.outputs)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'comm',
        'header': {'msg_type': 'comm'},
        'content': {
            'comm_id': 'foobar',
            # No 'state'
            'data': {'foo': 'bar'}
        }
    })
    def test_unknown_comm_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # An unknown comm message followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        # Widget states should be empty as the message has the wrong shape
        self.assertFalse(preprocessor.widget_state)
        self.assertFalse(preprocessor.widget_buffers)
        # Ensure no outputs were generated
        self.assertFalse(cell_mock.outputs)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'execute_result',
        'header': {'msg_type': 'execute_result'},
        'content': {
            'metadata': {'metafoo': 'metabar'},
            'data': {'foo': 'bar'},
            'execution_count': 42
        }
    })
    def test_execute_result_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # An execute followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        cell_mock.__setitem__.assert_called_once_with('execution_count', 42)
        # Should generate an associated message
        self.assertListEqual(cell_mock.outputs, [{
            'output_type': 'execute_result',
            'metadata': {'metafoo': 'metabar'},
            'data': {'foo': 'bar'},
            'execution_count': 42
        }])
        # No display id was provided
        self.assertFalse(preprocessor._display_id_map)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'execute_result',
        'header': {'msg_type': 'execute_result'},
        'content': {
            'transient': {'display_id': 'foobar'},
            'metadata': {'metafoo': 'metabar'},
            'data': {'foo': 'bar'},
            'execution_count': 42
        }
    })
    def test_execute_result_with_display_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # An execute followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        cell_mock.__setitem__.assert_called_once_with('execution_count', 42)
        # Should generate an associated message
        self.assertListEqual(cell_mock.outputs, [{
            'output_type': 'execute_result',
            'metadata': {'metafoo': 'metabar'},
            'data': {'foo': 'bar'},
            'execution_count': 42
        }])
        self.assertTrue('foobar' in preprocessor._display_id_map)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'display_data',
        'header': {'msg_type': 'display_data'},
        'content': {'metadata': {'metafoo': 'metabar'}, 'data': {'foo': 'bar'}}
    })
    def test_display_data_without_id_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # A display followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        # Should generate an associated message
        self.assertListEqual(cell_mock.outputs, [{
            'output_type': 'display_data',
            'metadata': {'metafoo': 'metabar'},
            'data': {'foo': 'bar'}
        }])
        # No display id was provided
        self.assertFalse(preprocessor._display_id_map)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'display_data',
        'header': {'msg_type': 'display_data'},
        'content': {
            'transient': {'display_id': 'foobar'},
            'metadata': {'metafoo': 'metabar'},
            'data': {'foo': 'bar'}
        }
    })
    def test_display_data_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # A display followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        # Should generate an associated message
        self.assertListEqual(cell_mock.outputs, [{
            'output_type': 'display_data',
            'metadata': {'metafoo': 'metabar'},
            'data': {'foo': 'bar'}
        }])
        self.assertTrue('foobar' in preprocessor._display_id_map)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'display_data',
        'header': {'msg_type': 'display_data'},
        'content': {
            'transient': {'display_id': 'foobar'},
            'metadata': {'metafoo': 'metabar'},
            'data': {'foo': 'bar'}
        }
    }, {
        'msg_type': 'display_data',
        'header': {'msg_type': 'display_data'},
        'content': {
            'transient': {'display_id': 'foobar'},
            'metadata': {'metafoo2': 'metabar2'},
            'data': {'foo': 'bar2', 'baz': 'foobarbaz'}
        }
    })
    def test_display_data_same_id_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # A display followed by an idle
        self.assertEqual(message_mock.call_count, 3)
        # Original output should be manipulated and a copy of the second now
        self.assertListEqual(cell_mock.outputs, [{
            'output_type': 'display_data',
            'metadata': {'metafoo2': 'metabar2'},
            'data': {'foo': 'bar2', 'baz': 'foobarbaz'}
        }, {
            'output_type': 'display_data',
            'metadata': {'metafoo2': 'metabar2'},
            'data': {'foo': 'bar2', 'baz': 'foobarbaz'}
        }])
        self.assertTrue('foobar' in preprocessor._display_id_map)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'update_display_data',
        'header': {'msg_type': 'update_display_data'},
        'content': {'metadata': {'metafoo': 'metabar'}, 'data': {'foo': 'bar'}}
    })
    def test_update_display_data_without_id_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # An update followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        # Display updates don't create any outputs
        self.assertFalse(cell_mock.outputs)
        # No display id was provided
        self.assertFalse(preprocessor._display_id_map)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'update_display_data',
        'header': {'msg_type': 'update_display_data'},
        'content': {
            'transient': {'display_id': 'foobar'},
            'metadata': {'metafoo2': 'metabar2'},
            'data': {'foo': 'bar2', 'baz': 'foobarbaz'}
        }
    })
    def test_update_display_data_mismatch_id_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # An update followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        # Display updates don't create any outputs
        self.assertFalse(cell_mock.outputs)
        # Display id wasn't found, so message was skipped
        self.assertFalse(preprocessor._display_id_map)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'display_data',
        'header': {'msg_type': 'display_data'},
        'content': {
            'transient': {'display_id': 'foobar'},
            'metadata': {'metafoo': 'metabar'},
            'data': {'foo': 'bar'}
        }
    }, {
        'msg_type': 'update_display_data',
        'header': {'msg_type': 'update_display_data'},
        'content': {
            'transient': {'display_id': 'foobar'},
            'metadata': {'metafoo2': 'metabar2'},
            'data': {'foo': 'bar2', 'baz': 'foobarbaz'}
        }
    })
    def test_update_display_data_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # A display followed by an update then an idle
        self.assertEqual(message_mock.call_count, 3)
        # Original output should be manipulated
        self.assertListEqual(cell_mock.outputs, [{
            'output_type': 'display_data',
            'metadata': {'metafoo2': 'metabar2'},
            'data': {'foo': 'bar2', 'baz': 'foobarbaz'}
        }])
        self.assertTrue('foobar' in preprocessor._display_id_map)

    @ExecuteTestBase.prepare_cell_mocks({
        'msg_type': 'error',
        'header': {'msg_type': 'error'},
        'content': {'ename': 'foo', 'evalue': 'bar', 'traceback': ['Boom']}
    })
    def test_error_message(self, preprocessor, cell_mock, message_mock):
        preprocessor.run_cell(cell_mock)
        # An error followed by an idle
        self.assertEqual(message_mock.call_count, 2)
        # Should also consume the message stream
        self.assertListEqual(cell_mock.outputs, [{
            'output_type': 'error',
            'ename': 'foo',
            'evalue': 'bar',
            'traceback': ['Boom']
        }])
