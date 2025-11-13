import boto3
import uuid
import os
import json
import traceback

def lambda_handler(event, context):
    try:
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Evento recibido",
                "evento": event
            }
        }))
        
        # Extraer datos del evento
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        # Crear estructura de la película
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }

        # Guardar en DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # Log de éxito
        print(json.dumps({
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Película creada correctamente",
                "pelicula": pelicula,
                "dynamodb_response": response
            }
        }))

        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }

    except Exception as e:
        # Log de error con traza
        print(json.dumps({
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Error al crear la película",
                "error": str(e),
                "traza": traceback.format_exc()
            }
        }))
        
        return {
            'statusCode': 500,
            'error': str(e)
        }
