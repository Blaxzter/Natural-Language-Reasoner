import os
import json

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response, FileResponse

from src.logics.NaturalTableauxSolver import NaturalTableauxSolver


def get_main_page(request):
    print(request)
    here = os.path.dirname(os.path.abspath(__file__))
    response = FileResponse(
        os.path.join(here, 'WebInterface.html'),
        request = request,
        content_type = 'text/html'
    )
    return response


def get_solve_request(request: Request):
    print(request.body)
    request = json.loads(request.body.decode("utf-8"))
    expressions = [data['value'] for data in request['expressions']]
    to_be_shown = request['to_be_shown']

    try:
        nts = NaturalTableauxSolver(expressions, to_be_shown)
        nts.solve()

        response = json.dumps(dict(
            applied_rules = [applied_rule.get_dict() for applied_rule in nts.get_applied_rules()],
            dot_graph = nts.get_dot_graph()
        ))
        return Response(response)
    except Exception as err:
        print(err)
        response = Response(str(err))
        response.status_int = 500
        return response


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('main', '/')
        config.add_route('solve-request', '/solve-request')
        config.add_view(get_main_page, route_name='main')
        config.add_view(get_solve_request, route_name='solve-request')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    print("Go to: http://localhost:6543")
    server.serve_forever()
