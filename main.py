import asyncio
import logging
import argparse


from aiomisc.log import basic_config

from aiohttp import web
from aiohttp.web import Application
import asyncpg
from setproctitle import setproctitle

from aiomisc import entrypoint

from utils import load_config, set_logging
from api import APIService

log = logging.getLogger()


async def finalize(app: Application):
    app["pool"].close()


def main():
    args = parser.parse_args()
    config = load_config(args.config)

    setproctitle(config["settings"]["proc_title"])

    basic_config(
        level=config["settings"]["log_level"],
        log_format='color',
        flush_interval=2
    )

    service = APIService(address=config["server"]["host"], port=config["server"]["port"], config=config)

    with entrypoint(service) as loop:
        loop.run_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple config comparing script')
    parser.add_argument('-c', '--config', type=str, required=False, help="path to config file", default="./config.toml")

    main()
