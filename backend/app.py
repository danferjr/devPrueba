import json


def lambda_handler(event, context):
    print("Evento recibido:", json.dumps(event))
   
    try:
        body = json.loads(event.get('body', '{}'))
        filename = body.get('filename')
        content = body.get('content')
       
        if not filename or not content:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Faltan campos 'filename' o 'content'"})
            }


        # Simulación (no guarda nada aún)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Archivo {filename} recibido correctamente."
            })
        }


    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
