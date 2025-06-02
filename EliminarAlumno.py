import boto3

def lambda_handler(event, context):
    # Entrada (json)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']

    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    # Eliminar el alumno
    response = table.delete_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        ReturnValues='ALL_OLD'
    )

    # Verificar si el alumno existía
    if 'Attributes' in response:
        mensaje = 'Alumno eliminado exitosamente'
        status = 200
    else:
        mensaje = 'Alumno no encontrado'
        status = 404

    # Salida (json)
    return {
        'statusCode': status,
        'message': mensaje,
        'response': response
    }
