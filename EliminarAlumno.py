import boto3
import json

def lambda_handler(event, context):
    print("Evento:", json.dumps(event))

    if not event.get('pathParameters') or not event['pathParameters'].get('alumno_id'):
        return {
            'statusCode': 400,
            'message': 'alumno_id es requerido en la URL'
        }

    alumno_id = event['pathParameters']['alumno_id']
    body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    tenant_id = body.get('tenant_id')

    if not tenant_id:
        return {
            'statusCode': 400,
            'message': 'tenant_id es requerido en el body'
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    response = table.delete_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        ReturnValues='ALL_OLD'
    )

    if 'Attributes' in response:
        mensaje = 'Alumno eliminado'
        status = 200
    else:
        mensaje = 'Alumno no encontrado'
        status = 404

    return {
        'statusCode': status,
        'message': mensaje,
        'response': response
    }
