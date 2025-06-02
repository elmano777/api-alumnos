import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Entrada (json)
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
