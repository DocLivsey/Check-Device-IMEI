import asyncio

import structlog

from settings import Settings
from imei_bot.IMEIbot import run

logger = structlog.get_logger(__name__)


def bot_logger(function):
    def wrapper(*args, **kwargs):
        logger.info(
            f'''
            Start running {function.__name__} 
            With settings and arguments
            ''',
            settings=f'{Settings}',
            args=args,
            kwargs=kwargs
        )
        try:
            return function(*args, **kwargs)
        except Exception as exc:
            logger.error('Exception occurred', exc_info=exc)

    return wrapper


@bot_logger
def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()