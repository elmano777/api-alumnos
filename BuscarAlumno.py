import boto3
import json

def lambda_handler(event, context):
    print(event)

    body = event['body']
    if isinstance(body, str):
        body = json.loads(body)

    tenant_id = body['tenant_id']
    alumno_id = body['alumno_id']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    response = table.get_item(
        Key={'tenant_id': tenant_id, 'alumno_id': alumno_id}
    )

    if 'Item' in response:
        return {
            'statusCode': 200,
            'alumno': response['Item']
        }
    else:
        return {
            'statusCode': 404,
            'message': 'Alumno no encontrado'
        }
