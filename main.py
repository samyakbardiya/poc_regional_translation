import logging
import sys

from loguru import logger
from uvicorn import Config, Server
from uvicorn.supervisors import ChangeReload

from toi_translation.settings import setting_cfg


"""
Unify Python logging for a Uvicorn/FastAPI application
https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
"""


class InterceptHandler(logging.Handler):
    """
    This code is copy-pasted from Loguru's documentation! This handler will be
    used to intercept the logs emitted by libraries and re-emit them through
    Loguru.
    """

    def emit(self, record):
        # get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(serialize):
    """
    Fix Python logging to use Loguru.
    https://github.com/encode/uvicorn/issues/1206#issuecomment-1173654956
    """

    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.getLevelName(setting_cfg.LOG_LEVEL))

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # specifically disable for some loggers
    for name in [
        "botocore.hooks",
        "botocore.loaders",
        "watchfiles.main",
    ]:
        # Specifically disable the 'watchfiles.main' logger
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = False
        # Effectively silences the logger
        logging.getLogger(name).setLevel(logging.CRITICAL + 1)

    # configure loguru
    logger.configure(
        handlers=[{"sink": sys.stdout, "colorize": True, "serialize": serialize}]
    )


class FixedLoggingConfig(Config):
    """Subclass of uvicorn config that re-configures logging."""

    serialize_logs = False

    def configure_logging(self) -> None:  # noqa: D102
        super().configure_logging()
        setup_logging(self.serialize_logs)


def run(
    host="0.0.0.0",
    port=8000,
    log_level=logging.getLevelName(setting_cfg.LOG_LEVEL),
    json_logs=setting_cfg.JSON_LOGS,
    reload=True,
    workers=1,
):
    """Run the Uvicorn server.

    Parameters:
        host: The host to bind.
        port: The port to use.
        log_level: The log level.
        json_logs: Whether to serialize logs in JSON.
        reload: Whether to enable live-reload.
    """
    FixedLoggingConfig.serialize_logs = json_logs
    config = FixedLoggingConfig(
        app="toi_translation.app:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
        workers=workers,
    )
    server = Server(config)
    setup_logging(serialize=json_logs)

    if reload:
        sock = config.bind_socket()
        ChangeReload(config, target=server.run, sockets=[sock]).run()
    else:
        server.run()


if __name__ == "__main__":
    run()
