"""Shared utilities module."""

import logging
import click


def init_logger():
    """Initializing a logger instance

    Args:

    Returns:
        logger instance
    Raises:
        None

    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('debug.log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    return logger


def get_logger():
    """Returning the logger instance

    Args:

    Returns:
        logger instance
    Raises:
        None

    """

    logger = logging.getLogger(__name__)
    return logger


def click_echo(message: str, from_cli: bool = False):
    """Echo message in CLI

    Args:

    Returns:
        True / False
    Raises:
        None

    """
    if from_cli:
        click.echo(message)
        return True
    return False
