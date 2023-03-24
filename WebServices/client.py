import requests
import json


def main():
    url = "http://localhost:4000/jsonrpc"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "getQty",
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(
        url, data=json.dumps(payload), headers=headers).json()

    # printing the response
    print(type(response['result']))


if __name__ == "__main__":
    main()