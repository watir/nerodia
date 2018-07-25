import logging
import os
import tempfile

import pytest

import nerodia


@pytest.fixture
def default_logging_handling():
    orig = nerodia.logger.level
    yield
    nerodia.logger.level = orig
    nerodia.logger.filename = None


@pytest.fixture
def filepath():
    filepath = os.path.join(tempfile.gettempdir(), 'log.tmp')
    yield filepath
    if os.path.isfile(filepath):
        os.remove(filepath)


def test_logs_warnings_by_default():
    assert nerodia.logger.level == logging.WARNING


@pytest.mark.usefixtures('default_logging_handling')
def test_allows_to_change_level_during_execution():
    nerodia.logger.level = logging.INFO
    assert nerodia.logger.level == logging.INFO
    assert logging.getLogger('nerodia').level == logging.INFO


@pytest.mark.usefixtures('default_logging_handling')
def test_allows_setting_level_by_integer():
    nerodia.logger.level = 5
    assert nerodia.logger.level == 5


@pytest.mark.usefixtures('default_logging_handling')
def test_allows_setting_level_by_string():
    nerodia.logger.level = 'critical'
    assert nerodia.logger.level == logging.CRITICAL


def test_outputs_to_stdout_by_default(caplog):
    nerodia.logger.warning('warning_message')
    assert 'warning_message' in caplog.text


def test_allows_to_output_to_file(filepath):
    nerodia.logger.filename = filepath
    nerodia.logger.warning('warning_message1')
    with open(filepath) as f:
        text = f.read()
    assert 'warning_message1' in text

    nerodia.logger.warning('warning_message2')
    with open(filepath) as f:
        text = f.read()
    nerodia.logger.filename = None  # close file
    assert 'warning_message2' in text


def test_allows_stopping_output_to_file(filepath):
    nerodia.logger.filename = filepath
    nerodia.logger.warning('warning_message1')
    with open(filepath) as f:
        text = f.read()
    assert 'warning_message1' in text

    nerodia.logger.filename = None

    nerodia.logger.warning('warning_message2')
    with open(filepath) as f:
        text = f.read()
    assert 'warning_message2' not in text


def test_allows_to_deprecate_functionality(caplog):
    nerodia.logger.deprecate('#old', '#new')
    assert '[DEPRECATION] #old is deprecated. Use #new instead.' in caplog.text


def test_allows_to_selectively_ignore_deprecations(caplog):
    nerodia.logger.ignore('old deprecated')
    nerodia.logger.deprecate('#old', '#new', ids=['old deprecated'])
    assert '#old' not in caplog.text
    assert '#new' not in caplog.text


def test_allows_to_selectively_ignore_warnings(caplog):
    nerodia.logger.ignore('spam')
    nerodia.logger.warning('WARNING HAM', ids=['spam'])
    assert 'WARNING HAM' not in caplog.text


def test_allows_to_ignore_all_deprecation_notices(caplog):
    nerodia.logger.ignore('deprecations')
    nerodia.logger.deprecate('#old', '#new')
    assert '#old' not in caplog.text
    assert '#new' not in caplog.text


def test_allows_to_ignore_multiple_ids(caplog):
    nerodia.logger.ignore('spam', 'ham')
    nerodia.logger.warning('WARNING SPAM', ids=['spam'])
    nerodia.logger.warning('WARNING HAM', ids=['ham'])
    assert 'WARNING HAM' not in caplog.text
    assert 'WARNING SPAM' not in caplog.text

