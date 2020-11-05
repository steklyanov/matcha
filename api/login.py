# from aiohttp import
from aiohttp.web import Application


class Login:
    def __init__(self):
        pass

    def declare_routes(self, app: Application):
        app.router.add_route('GET', '/get-user', self.protected_page)
        app.router.add_route('POST', '/login', self.login)
