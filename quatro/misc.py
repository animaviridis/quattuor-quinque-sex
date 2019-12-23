import logging
import coloredlogs


def log_exceptions(log_name=None):
    logger = logging.getLogger(log_name or __name__)
    coloredlogs.install(level='DEBUG', logger=logger)

    def decorator(func):
        def wrapper(*args, **kwargs):
            ret = None

            try:
                ret = func(*args, **kwargs)
            except (TypeError, ValueError, RuntimeError, IndexError) as e:
                logger.error(f"{e}")

            return ret

        return wrapper
    return decorator
