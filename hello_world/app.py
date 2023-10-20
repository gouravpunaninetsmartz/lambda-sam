import json
import requests
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import event_parser, BaseModel


logger = Logger()

# class QueryParameter(BaseModel):
#         queryStringParameters: {"startPeriod": str,}

# @event_parser(model=QueryParameter)
def lambda_handler(event, context):

    #setting log message for function invocation
    logger.info("lambda function invoked")

    # Check if variable1 is empty or not provided
     # Access query variables
    query_parameters = event.get("queryStringParameters", {})
    startPeriod = query_parameters.get("startPeriod", "")
    if startPeriod is None or startPeriod.strip() == "":
        startPeriod = "2012"  # Set the default value

    
    # define variable for storing interest values
    interest = []

    try:
        api_url = f"https://api.data.abs.gov.au/data/CPI/1.10001.10.50.Q?startPeriod={startPeriod}-Q1&format=jsondata"
        response = requests.get(api_url)

        if response.status_code == 200:
            # print(response.json())  # Assuming the response is in JSON format
            data = response.json()
            # observations = data.dataSets[0].series."0:0:0:0:0".observations[]
            data_sets = data.get("data", {}).get("dataSets", [])

            if data_sets and len(data_sets) > 0:
                series = data_sets[0].get("series", {}).get("0:0:0:0:0", {})
                observations = series.get("observations", {})
                # parser = Parser(observations, schema = {str: [str, None, str, None]})
                # parsed_observations = parser.parse()

                for index, values in observations.items():
                    if values and len(values) > 0:
                        first_item = values[0]
                        interest.append(first_item)

            print('interest', interest)
            
        else:
            print(f"API request failed with status code: {response.status_code}")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            "interest": interest
        }),
    }
