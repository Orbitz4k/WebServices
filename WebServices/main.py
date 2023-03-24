from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


class getAllData(Resource):
    def get(self):
        import mysql.connector

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="example",
            port=2222,
            database='microservice'
        )
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM products")

        buffer = ''
        for x in mycursor:
            print(x)

            id = x[0]
            name = x[1]

            jsonContent = '{"id": ' + str(id) + ', "name": "' + name + '"}'
            print(jsonContent)
            buffer += jsonContent + ','

        buffer = buffer[:-1]  # remove last comma
        import json
        jsonFinal = json.loads(buffer)
        print(jsonFinal)
        return jsonFinal


api.add_resource(getAllData, '/getAllData')


# getStockIDs endpoint
class getStockIDs(Resource):
    def get(self):
        outputBuffer = '{"code": ['  # put all the content to send back

        file1 = open("products.txt", "r")
        content = file1.readlines()  # getting the lines of the file
        for line in content:  # for each line in the file
            # print(line)
            # spltting the line and turns line into an array everywhere it finds a dash
            prodCode = line.split('-')
            print(prodCode[0])  # prints the first element of the array

            # For every product code, make a new element in the buffer of the json
            outputBuffer += '' + prodCode[0] + ', '

        outputBuffer += ' 666] }'
        print(outputBuffer)
        import json
        return json.loads(outputBuffer)


api.add_resource(getStockIDs, '/getStockIDs')


class getStockNames(Resource):
    def get(self):

        import pymongo
        myclient = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
        mydb = myclient["products"]
        products = mydb["products"]

        buffer = '{'

        for x in products.find():
            if "item" in x:
                print(x["item"])
                buffer += '"' + x["item"] + '",'

        buffer = buffer[:-1]  # remove last comma
        buffer += ']}'

        return buffer


api.add_resource(getStockNames, '/getStockNames')


class placeOrder(Resource):
    def get(self):
        content = request.args.get('param')
        import base64
        print(base64.b64decode(content))

        import pika

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='hello')

        channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
        print(" [x] Sent 'Hello World!'")
        connection.close()

        return {'hello': 'world'}


api.add_resource(placeOrder, '/placeOrder')

if __name__ == '__main__':
    app.run(debug=True)