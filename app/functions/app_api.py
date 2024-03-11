import json


def handle(event, context):
    result = {"statusCode": 200,
              "body": json.dumps({"msg": "Success"})}
    return result
