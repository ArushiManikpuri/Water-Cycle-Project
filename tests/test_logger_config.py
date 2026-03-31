import logging
import os
import shutil
import pytest
from logger_config import setup_logger


@pytest.fixture(autouse=True)
def cleanup_logs():
    """Remove the logs directory before and after each test."""
    if os.path.exists("logs"):
        shutil.rmtree("logs")
    yield
    if os.path.exists("logs"):
        shutil.rmtree("logs")


@pytest.fixture(autouse=True)
def reset_loggers():
    """Remove all handlers from loggers created during tests."""
    yield
    for name in ("test_logger", "duplicate_logger", "another_logger"):
        logger = logging.getLogger(name)
        logger.handlers.clear()


class TestSetupLogger:
    def test_returns_logger_instance(self):
        logger = setup_logger("test_logger")
        assert isinstance(logger, logging.Logger)

    def test_logger_has_correct_name(self):
        logger = setup_logger("test_logger")
        assert logger.name == "test_logger"

    def test_logger_level_is_info(self):
        logger = setup_logger("test_logger")
        assert logger.level == logging.INFO

    def test_creates_logs_directory(self):
        setup_logger("test_logger")
        assert os.path.isdir("logs")

    def test_creates_log_file(self):
        setup_logger("test_logger")
        assert os.path.isfile("logs/test_logger.log")

    def test_logger_has_two_handlers(self):
        logger = setup_logger("test_logger")
        assert len(logger.handlers) == 2

    def test_logger_has_stream_handler(self):
        logger = setup_logger("test_logger")
        handler_types = [type(h) for h in logger.handlers]
        assert logging.StreamHandler in handler_types

    def test_logger_has_file_handler(self):
        logger = setup_logger("test_logger")
        handler_types = [type(h) for h in logger.handlers]
        assert logging.FileHandler in handler_types

    def test_no_duplicate_handlers_on_repeated_calls(self):
        setup_logger("duplicate_logger")
        logger = setup_logger("duplicate_logger")
        assert len(logger.handlers) == 2

    def test_log_message_written_to_file(self):
        logger = setup_logger("test_logger")
        logger.info("test message")
        with open("logs/test_logger.log") as f:
            contents = f.read()
        assert "test message" in contents

    def test_different_loggers_are_independent(self):
        logger1 = setup_logger("test_logger")
        logger2 = setup_logger("another_logger")
        assert logger1.name != logger2.name
        assert os.path.isfile("logs/test_logger.log")
        assert os.path.isfile("logs/another_logger.log")
