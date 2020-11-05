import asyncio
import logging
import argparse


from aiohttp import web
from aiohttp.web import Application
import asyncpg
from setproctitle import setproctitle

from utils import load_config, set_logging


async def init(args: argparse.Namespace):
    setproctitle("matcha_backend")
    config = load_config(args.config)
    set_logging(config)

    app = web.Application()

    app["pool"] = await asyncpg.create_pool(user=config['database']['username'],
                                            password=config['database']['password'],
                                            database=config['database']['dbname'],
                                            host=config['database']['host'],
                                            port=config['database']['port'])

    app["config"] = config

    return app, config


async def finalize(app: Application):
    app["pool"].close()


def main():
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    app, config = loop.run_until_complete(init(args))

    app.on_cleanup.append(finalize)

    web.run_app(app, host=config["server"]["host"], port=config["server"]["port"], access_log=logging.Logger)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple config comparing script')
    parser.add_argument('-c', '--config', type=str, required=False, help="path to config file", default="./config.toml")

    main()
