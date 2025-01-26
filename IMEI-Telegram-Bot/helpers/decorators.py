import structlog

logger = structlog.get_logger(__name__)


def bot_logger(function):
    def wrapper(*args, **kwargs):
        logger.info(
            f'''
            Start running {function.__name__}() 
            With arguments
            ''',
            args=args,
            kwargs=kwargs
        )
        try:
            return function(*args, **kwargs)
        except Exception as exc:
            logger.error('Exception occurred', exc_info=exc)

    return wrapper