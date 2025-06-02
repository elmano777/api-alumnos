import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    print("EVENT:", event)

    # Convertir el body a dict si viene como string
    if isinstance(event.get('body'), str):
        body = json.loads(event['body'])
    else:
        body = event.get('body', {})

    # Validación
    if not event.get('pathParameters') or not event['pathParameters'].get('alumno_id'):
        return {
            'statusCode': 400,
            'message': 'alumno_id es requerido en la URL'
        }

    alumno_id = event['pathParameters']['alumno_id']
    tenant_id = body.get('tenant_id')
    alumno_datos = body.get('alumno_datos')

    if not tenant_id or not alumno_datos:
        return {
            'statusCode': 400,
            'message': 'tenant_id y alumno_datos son requeridos en el cuerpo'
        }

    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    table.put_item(
        Item={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id,
            'alumno_datos': alumno_datos
        }
    )

    return {
        'statusCode': 200,
        'message': f'Alumno {alumno_id} modificado correctamente'
    }
