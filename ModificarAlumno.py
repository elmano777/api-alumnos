import boto3
import json

def lambda_handler(event, context):
    print(event)

    body = event['body']
    if isinstance(body, str):  # Por si API Gateway lo manda como string
        body = json.loads(body)
    
    tenant_id = body['tenant_id']
    alumno_id = body['alumno_id']
    nuevos_datos = body['alumno_datos']  # reemplaza el campo completo

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    response = table.update_item(
        Key={'tenant_id': tenant_id, 'alumno_id': alumno_id},
        UpdateExpression="SET alumno_datos = :val1",
        ExpressionAttributeValues={":val1": nuevos_datos}
    )

    return {
        'statusCode': 200,
        'message': f'Alumno {alumno_id} modificado correctamente'
    }
