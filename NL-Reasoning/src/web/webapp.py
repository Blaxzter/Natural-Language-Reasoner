"""
File containing the boilerplate pyramid server
"""

import os
import json
import traceback

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.response import Response, FileResponse

from logics.NaturalTableauxSolver import NaturalTableauxSolver
from logics.senteces.Helper import create_expression, create_expression_representation
from logics.senteces.ParseExceptions import ParseException


def get_main_page(request):
    """
    Get the root file main page
    :param request: The request
    :return: The response containing the WebInterface
    """
    print(request)
    here = os.path.dirname(os.path.abspath(__file__))
    response = FileResponse(
        os.path.join(here, 'files/WebInterface.html'),
        request = request,
        content_type = 'text/html'
    )
    return response


def get_file(request):
    """
    Function for the data sets that returns the data sets as files
    """
    print(request)
    here = os.path.dirname(os.path.abspath(__file__))
    response = FileResponse(
        os.path.join(here, f'files/{request.GET["name"]}'),
        request = request,
        content_type = 'application/json'
    )
    return response


def get_language_request(request: Request):
    """
    Handels the language parse request
    :param request: The request
    :return: The parse setnece or an exception
    """
    request = json.loads(request.body.decode("utf-8"))
    sentence = request['sentence']

    try:
        expression = create_expression(sentence)
        representation = create_expression_representation(expression)

        response = json.dumps(representation)
        return Response(response)
    except Exception as err:
        traceback.print_exc()
        response = Response(str(dict(
            type = type(err).__name__,
            list = "null" if type(err) is not ParseException else err.exception_list,
            error = str(err)
        )))
        response.status_int = 500
        return response


def get_solve_request(request: Request):
    request = json.loads(request.body.decode("utf-8"))
    expressions = [data['value'] for data in request['expressions']]
    to_be_shown = request['to_be_shown']

    try:
        nts = NaturalTableauxSolver(expressions, to_be_shown)
        nts.solve()

        response = json.dumps(dict(
            applied_rules = {i: applied_rule.get_dict() for i, applied_rule in nts.get_applied_rules().items()},
            all_branches_closed = nts.tableaux_is_closed(),
            dot_graph = nts.get_dot_graph())
        )
        return Response(response)
    except Exception as err:
        traceback.print_exc()
        response = Response(str(dict(
            type = type(err).__name__,
            list = "null" if type(err) is not ParseException else err.exception_list,
            error = str(err)
        )))
        response.status_int = 500
        return response


def start_web_server():
    with Configurator() as config:
        config.add_route('main', '/')
        config.add_route('solve-request', '/solve-request')
        config.add_route('examples', '/examples')
        config.add_route('language-request', '/language-request')

        config.add_view(get_main_page, route_name = 'main')
        config.add_view(get_solve_request, route_name = 'solve-request')
        config.add_view(get_language_request, route_name = 'language-request')
        config.add_view(get_file, route_name = 'examples', http_cache = 0)

        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    print("Go to: http://localhost:6543")
    server.serve_forever()
