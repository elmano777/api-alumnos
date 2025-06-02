import boto3
import json

def lambda_handler(event, context):
    print("Evento:", json.dumps(event))  # Para depurar

    # Validar parámetros
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

    # DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')

    # Aquí modificamos campos específicos, por ejemplo "nombre"
    update_expression = "SET nombre = :nombre"
    expression_values = {
        ":nombre": body.get('nombre', 'Sin nombre')
    }

    response = table.update_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
        ReturnValues='ALL_NEW'
    )

    return {
        'statusCode': 200,
        'message': 'Alumno actualizado',
        'alumno': response.get('Attributes', {})
    }
