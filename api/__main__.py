from aiohttp import web
from aiomisc.service.aiohttp import AIOHTTPService
import asyncpg
from aiohttp_jwt import JWTMiddleware
import logging
from datetime import datetime, timedelta

import jwt

from api.v1.auth import Auth

log = logging.getLogger(__name__)


class APIService(AIOHTTPService):
    """ Docstring """

    async def create_application(self):
        app = web.Application(
            middlewares=[JWTMiddleware(self.config["settings"]["secret"],
                                       whitelist=[r"/public*"]),
                         ]
        )
        log.info("Create app")

        app["pool"] = await asyncpg.create_pool(user=self.config['database']['username'],
                                                password=self.config['database']['password'],
                                                database=self.config['database']['dbname'],
                                                host=self.config['database']['host'],
                                                port=self.config['database']['port'])

        log.info("Create pool")
        auth = Auth(self.config)
        app = await auth.create_routes(app)

        await self.create_routes(app)

        return app

    async def create_routes(self, app):
        """
        Create all necessary routes
        :param app:
        """
        app.router.add_get("/public", self.public_handler)
        app.router.add_get("/protected", self.protected_handler)



    async def public_handler(self, request):
        log.info("get public request")
        return web.json_response({"username": "anonymous"})

    async def protected_handler(self, request):
        return web.json_response({"username": request["user"].get("username", "anonymous")})
