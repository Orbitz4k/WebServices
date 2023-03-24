from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher


@dispatcher.add_method(name="getQty")
def getQty(**kwargs):

    f = open('products.txt', 'r')

    content = f.readlines()
    buffer = '{ "products": ['

    for oneline in content:
        print(oneline)

        contentElements = oneline.split('-')[2]
        print(contentElements)
        buffer += contentElements + ','

    buffer = buffer[:-1] # remove last comma
    buffer += ']}'
    print(buffer)

    import json
    # loads takes from string and returns to json
    return json.loads(buffer)

@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["echo"] = lambda s: s
    dispatcher["add"] = lambda a, b: a + b
    dispatcher["getQty"] = getQty

    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)