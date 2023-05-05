import logging

from rich.logging import RichHandler


logging.basicConfig(
    level=logging.CRITICAL,
    format="\[%(module)s.%(funcName)s] %(message)s",
    # handlers=[RichHandler(markup=True)],
)


