import asyncio

from imei_bot.IMEIbot import run
from helpers.decorators import bot_logger


@bot_logger
def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()