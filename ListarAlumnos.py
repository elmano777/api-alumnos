import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Entrada (json)
    print("Event:", event)  # Para debug
    
    # Validar queryStringParameters
    if not event.get('queryStringParameters') or not event['queryStringParameters'].get('tenant_id'):
        return {
            'statusCode': 400,
            'message': 'tenant_id es requerido como query parameter'
        }
    
    # Validar pathParameters
    if not event.get('pathParameters') or not event['pathParameters'].get('alumno_id'):
        return {
            'statusCode': 400,
            'message': 'alumno_id es requerido en la URL'
        }
    
    tenant_id = event['queryStringParameters']['tenant_id']
    alumno_id = event['pathParameters']['alumno_id']
    
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    
    # Buscar el alumno específico
    response = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )
    
    # Verificar si el alumno existe
    if 'Item' in response:
        alumno = response['Item']
        mensaje = 'Alumno encontrado'
        status = 200
    else:
        alumno = None
        mensaje = 'Alumno no encontrado'
        status = 404
    
    # Salida (json)
    return {
        'statusCode': status,
        'message': mensaje,
        'alumno': alumno
    }
