import joblib
import boto3
import io
import scikeras
import json

def get_model():
    s3 = boto3.client('s3')
    model = s3.get_object(Bucket='covid-models-4288', Key='modelo_gru_latest.joblib')
    model_bytes = model['Body'].read()
    loaded_model = joblib.load(io.BytesIO(model_bytes))
    return loaded_model

def get_scaler_data():
    s3 = boto3.client('s3')
    model = s3.get_object(Bucket='covid-models-4288', Key='scaler.joblib')
    model_bytes = model['Body'].read()
    loaded_model = joblib.load(io.BytesIO(model_bytes))
    return loaded_model

def get_scaler_feature():
    s3 = boto3.client('s3')
    model = s3.get_object(Bucket='covid-models-4288', Key='scaler_feature.joblib')
    model_bytes = model['Body'].read()
    loaded_model = joblib.load(io.BytesIO(model_bytes))
    return loaded_model

def scaler_data(data):
    model = get_scaler_data()
    data_scaled = model.fit_transform(data)
    return data_scaled

def lambda_handler(event, context):
    """
    Carrega um modelo Joblib do S3 e realiza predições em um ambiente Lambda.

    Args:
        event (dict): O evento que desencadeia a execução da função Lambda.
        context (LambdaContext): O contexto de execução da função Lambda.

    Returns:
        dict: Um dicionário contendo as predições.
    """
    
    
    # Baixa o modelo do S3 para um objeto em memória
    
    import numpy as np
    path = event['path']

    if 'arr' in event and '/predict' in path:
        print("iniciando")
        array = np.array(event['arr'])
        array = scaler_data(array)
        array = np.expand_dims(array, axis=0)
        s3 = boto3.client('s3')
        loaded_model = get_model()
        # Realiza as predições
        predictions = loaded_model.predict(array)
        sc_feature = get_scaler_feature()
        predictions = sc_feature.inverse_transform(predictions.reshape(-1, 1))
        print(sc_feature.inverse_transform(predictions.reshape(-1, 1)))
        return {
            'statusCode': 200,
            'body': str(predictions)
        }
    return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,GET'
                },
            }