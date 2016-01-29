import falcon
from wsgiref import simple_server

import leaderboard
import root

ALLOWED_ORIGINS = ['http://0.0.0.0:5000']  # Or load this from a config file


class CorsMiddleware(object):

    def process_request(self, request, response):
        origin = request.get_header('Origin')
        if origin in ALLOWED_ORIGINS:
            response.set_header('Access-Control-Allow-Origin', origin)


app = falcon.API(middleware=[CorsMiddleware()])
root = root.RootItem()
board = leaderboard.LeaderboardItem()

app.add_route('/', root)
app.add_route('/v1.0/{org}/{repo}/leaderboard/', board)


msgtmpl = (u'Serving on host %(bind)s:%(port)s')
print(msgtmpl,
      {'bind': "0.0.0.0", 'port': "8888"})

httpd = simple_server.make_server("0.0.0.0",
                                  8888,
                                  app)
httpd.serve_forever()
