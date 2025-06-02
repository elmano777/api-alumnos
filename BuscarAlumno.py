import boto3
import json

def lambda_handler(event, context):
    print("Evento:", json.dumps(event))

    if not event.get('pathParameters') or not event['pathParameters'].get('alumno_id'):
        return {
            'statusCode': 400,
            'message': 'alumno_id es requerido en la URL'
        }

    if not event.get('queryStringParameters') or not event['queryStringParameters'].get('tenant_id'):
        return {
            'statusCode': 400,
            'message': 'tenant_id es requerido como query parameter'
        }

    alumno_id = event['pathParameters']['alumno_id']
    tenant_id = event['queryStringParameters']['tenant_id']

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )

    if 'Item' in response:
        alumno = response['Item']
        status = 200
        mensaje = 'Alumno encontrado'
    else:
        alumno = None
        status = 404
        mensaje = 'Alumno no encontrado'

    return {
        'statusCode': status,
        'message': mensaje,
        'alumno': alumno
    }
