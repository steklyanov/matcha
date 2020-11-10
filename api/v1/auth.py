# from api.base import BaseView
from aiohttp import web
import logging
import jwt
from datetime import datetime, timedelta

log = logging.getLogger(__name__)


class Auth:
    def __init__(self, config):
        self.JWT_EXP_DELTA_SECONDS = config["auth"]["expr_delta"]
        self.JWT_ALGORITHM = config["auth"]["algo"]
        self.JWT_SECRET = config["auth"]["secret"]
    pass

    async def create_routes(self, app: web.Application) -> web.Application:
        app.router.add_post("/public_login", self.login)
        app.router.add_get("/logout", self.logout)
        app.router.add_patch("/refresh", self.refresh_token)

        return app

    async def login(self, request):
        log.info(f'Receive request for user login')
        post_data = await request.json()
        if not post_data:
            return web.json_response({"results": "No data provided"})
        log.info(post_data)
        login = post_data.get('login')
        provided_password = post_data.get('password')
        if login and provided_password:
            data = await self.user_model.select_single('login', login)
            if len(data) and await self.user_model.verify_password(data[0]["password"], provided_password):
                payload = {
                    'id': str(data[0]["id"]),
                    'is_superuser': str(data[0]["is_superuser"]),
                    'exp': datetime.utcnow() + timedelta(seconds=self.JWT_EXP_DELTA_SECONDS)
                }
                jwt_token = jwt.encode(payload, self.JWT_SECRET, self.JWT_ALGORITHM)
                return web.json_response({"token": jwt_token.decode('utf-8')})
            return web.json_response({"results": "Invalid login or password"})
        return web.json_response({"results": "No login or password provided"})

    async def logout(self):
        pass

    async def refresh_token(self):
        pass

