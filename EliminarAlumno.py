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

    table.delete_item(
        Key={'tenant_id': tenant_id, 'alumno_id': alumno_id}
    )

    return {
        'statusCode': 200,
        'message': f'Alumno {alumno_id} eliminado correctamente'
    }
