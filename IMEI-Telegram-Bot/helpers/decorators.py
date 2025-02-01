import asyncio

import structlog

logger = structlog.get_logger(__name__)


def bot_logger(function):
    
    def sync_wrapper(*args, **kwargs):
        logger.info(
            f'''
            Start running sync {function.__name__}() 
            With arguments
            ''',
            args=args,
            kwargs=kwargs
        )
        try:
            return function(*args, **kwargs)
        except Exception as exc:
            logger.error(
                'Exception occurred in sync process', 
                exc_info=exc
            )
    
    async def async_wrapper(*args, **kwargs):
        logger.info(
            f'''
            Start running async {function.__name__}() 
            With arguments
            ''',
            args=args,
            kwargs=kwargs
        )
        try:
            return await function(*args, **kwargs)
        except Exception as exc:
            logger.error(
                'Exception occurred in async process', 
                exc_info=exc
            )

    return async_wrapper \
        if asyncio.iscoroutinefunction(function.__wrapped__ if hasattr(function, '__wrapped__') else function) \
        else sync_wrapper