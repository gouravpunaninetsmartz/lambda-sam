# Answers


The questions in this document are intended as a minimal guide only: please
extend them with your own thoughts on tooling, architecture and troubleshooting.


## Part 1: Your Local Environment


### Task 1: Set up Docker


**Document the process you used to set up Docker.**


Step 1: Download & Install Docker
I’m working on Windows, I’d docker already installed in my system. I’d followed their official get started page https://www.docker.com/get-started/ where it’s just one click download and you can simply install the docker by selecting some default configuration.


Step 2: Docker Configuration


Docker Engine Configuration:
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "features": {
    "buildkit": true
  }
}
Resources: by default docker is using the WSL 2 backend, so resource limits are managed by Windows.


Docker Version: 24.0.2


Step 3: Verify Installation
I simply run the docker –version command ot confirm successful installation of docker and it returns the current docker version in my system.




### Task 2: Set up a Python virtual environment


**Document the process you used to set up Python.**


I’d python already installed in my stem. I checked for the python verion and confirm installation using python –version command.
Python version before: 3.8


...


**Document the process you used to set up your Python virtual environment.**
For python virtual enviornment I choosed to go with pyenv. I found some difficulty installing the pyenv on windows from github repo as it had difficult for me to grap the all step required so I R&D on pyenv documentation for windows, I found this website https://pypi.org/project/pyenv-win/ which had much better clear step on how to install pyenv on windows.

I followed these steps to install pyenv on windows.


First I Install pyenv using power with this command


Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"




In order to use pyenv from command prompt or access pyenv globally I setup thes window env variables for pyenv


System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")


[System.Environment]::SetEnvironmentVariable('PYENV_ROOT',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")


[System.Environment]::SetEnvironmentVariable('PYENV_HOME',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")


[System.Environment]::SetEnvironmentVariable('path', $env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE + "\.pyenv\pyenv-win\shims;" + [System.Environment]::GetEnvironmentVariable('path', "User"),"User")


After executing these commands, I was able to access pyenv from command prompt directly without having to pass the pyenv installation path in each command.


Further I checked for my python and pyenv version. To work on the task, I changed my python global version to 3.11 using the command:


pyenv install 3.11.0 (for installing) and
pyenv global 3.11.0 for setting up the global python verion to 3.11.0








...


### Task 3: The AWS SAM CLI


**Document the process you used to set up the SAM CLI.**


I followed the aws sam official documentation page for windows 64 bit.
Link: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html


After installing the download setup, I was able to access the aws sam from command line. I confirmed the installation by using command: sam


...


## Part 2: Application Scaffolding


### Task 1: Project setup


**Document the steps taken to get the Hello World application running.**


In order to initialize the hello world application for serverless application I used sam and run command


sam init


It gives few prompts to select from like template, X-Ray tracing etc. After running the command, it create project folder with hello world function in it.


I used sam build command to build the project but got the error: build failed. After troubleshooting for some time, I found the solution that we need to pass the –use-container flag in order to run it in a containerized manner. then I used the command


sam init –use-container


Once the build was generated successfully, I used sam local invoke command to invoke the lambda function locally and it returns the default json dump from app.py hello_world function.


...


**Document the steps taken in troubleshooting `sam local invoke`, if any.**


while using the sam local invoke command, I got the request timeout issue several times, I troubleshoot the issue and checked we can increase the timeout for the function in template.yml file directly for the global scope for function. I modified the Timeout property in Globals to increase the execution time.


...


**Record the output of `sam local invoke`.**
START RequestId: 24dfa305-2c83-4892-bcee-7645200b0f6d Version: $LATEST
{"level":"INFO","location":"lambda_handler:16","message":"lambda function invoked","timestamp":"2023-10-20 07:50:24,958+0000","service":"service_undefined"}
interest ['99.9', '100.4', '101.8', '102', '102.4', '102.8', '104', '104.8', '105.4', '105.9', 
'106.4', '106.6', '106.8', '107.5', '108', '108.4', '108.2', '108.6', '109.4', '110', '110.5', 
'110.7', '111.4', '112.1', '112.6', '113', '113.5', '114.1', '114.1', '114.8', '115.4', '116.2', '116.6', '114.4', '116.2', '117.2', '117.9', '118.8', '119.7', '121.3', '123.9', '126.1', '128.4', '130.8', '132.6', '133.7']
END RequestId: 24dfa305-2c83-4892-bcee-7645200b0f6d
REPORT RequestId: 24dfa305-2c83-4892-bcee-7645200b0f6d  Init Duration: 0.10 ms  Duration: 3796.09 ms   Billed Duration: 3797 ms        Memory Size: 128 MB     Max Memory Used: 128 MB        
{"statusCode": 200, "body": "{\"message\": \"hello world test\", \"interest\": [\"99.9\", \"100.4\", \"101.8\", \"102\", \"102.4\", \"102.8\", \"104\", \"104.8\", \"105.4\", \"105.9\", \"106.4\", \"106.6\", \"106.8\", \"107.5\", \"108\", \"108.4\", \"108.2\", \"108.6\", \"109.4\", \"110\", \"110.5\", \"110.7\", \"111.4\", \"112.1\", \"112.6\", \"113\", \"113.5\", \"114.1\", \"114.1\", \"114.8\", \"115.4\", \"116.2\", \"116.6\", \"114.4\", \"116.2\", \"117.2\", \"117.9\", \"118.8\", \"119.7\", \"121.3\", \"123.9\", \"126.1\", \"128.4\", \"130.8\", \"132.6\", \"133.7\"]}"}






...


### Task 2: Run tests


**Why do the integration tests fail?**


Integration test fail due to missing field in env AWS_SAM_STACK_NAME. to resolve this issue we can set the AWS_SAM_STACK_NAME in enviornment variables using command export AWS_SAM_STACK_NAME=your-stack-name
Exact error: ValueError: Please set the AWS_SAM_STACK_NAME environment variable to the name of your stack




**How we can run `pytest` on only the unit tests?**


To run only unit tests, we can use the -m option with the not expression to exclude the integration tests:


Command: pytest -m "not integration"




...


### Task 3: Powertools


**What problem does this library solve?**
Powertool library helps in Logging and Monitoring  and parsing data for lambda functions. It helps in validating the incoming bound and parse the input data. It also helps in monitoring the logs on aws cloudwatch and other aws services.
...


**How would you consume the output of these logs?**
By default, AWS Lambda logs are sent to aws cloudwatch logs. we can access these logs through the AWS Management Console or using the aws-sdk as well. We can also setup log policies to retain, customize and do further operations in cloudwatch.
...


## Part 3: Let's Build


### Task 1: Fetching data


**How did you decide this approach to fetching data?**
I used requests library from python to make an HTTP request to an external api. This is a common and straightforward way to fetch data from external sources. it provides error handling for both request and exception that might occur in api call.
...


**If we had to make 1,000 API requests in this function invocation, how would
you modify your approach?**


To efficiently make 1,000 API requests, we can do the batch processing. Instead of making 1000 API call serially, we can group multiple requests into a single batch and send them together. This approach reduces the overhead of invoking the API for each request. In reference to lamda function, we can also call the lambda function concurrently. We can configure our lamda function to handle different level of concurrency though it will scale up the lambda server & may result in higher cost.


...


**If this API used bearer token authentication, how would you modify your
approach? How would you handle the `client_secret`?**


We can leverage the aws ssm parameter store to store and retrieve the client_secret. We can grant our lambda function permission to access the desired data. Also bearer token might have expiry time so I’ll also implement the token refresh functionality using by calling api with refresh_token to get new token.


...


**How would you cache responses from this API?**


We can use cache tools library from Python to cache the responses for this api. It helps us setting the cache by the key (dictionary concept) which we can use to cache our request by startPeriod so if user request the data for same startPeriod, we can provide the cached data from storage.


### Task 2: Validating data


**What are the downsides of `json.loads` and `json.dumps`? What is a better
approach to serialization?**

there are few downsides of using json.loads and json.dumps method for serialization/deserialization.
- json is a text-based format and it has limited data type so it does not support Python native complex data types like datetime objects, sets etc..
- both methods are generally fast by may lag in performance for large and complex data.
- custom  Serialization/Deserialization is difficult with these as well


Approach for serialization:


A better approach to serialization often depends on the specific use case and requirements. 
for complex data structure w can implement custom serialization . we can use to_json to serialize from_json to deserialize.


we can also use third party libraries like Marshmallow to handle serialization better  as well.
for performance-critical applications, we might use binary serializations.





### Task 3: Triggering via API


In order to simulate api gateway locally we can use sam local start-api. This command will create a server locally on port 3000 with function name as url/function_name in order to test it locally. We can also modify the port for the local server in events/event.json file for the lambda function.


**Assume this lambda is one of many in a data processing pipeline. What
architecture would you suggest to trigger each function in order?**


We can use AWS step functions for such kind of requirement. It's a fully managed AWS serverless application that we can use to create and run workflows and execute lambda functions in a specific order.


we can also use AWS Eventbridge for the same. it's also a server by aws to create event bus service where we can route to various aws services based on specified conditions. In our case, we can use it to trigger lamda functions in a specific order by defining event rules and targets for functions in order.






**Validation


I was facing some issue with powertool parser validation so I excluded that part of code from the script so that function can be build & executed properly. In typescript, I would have use the following steps to validate the inbounds in handler and run time validation:


Handler inbound 


interface Observation{
  observations: {
    [key: string]: [number, null, number, null];
  };
}

import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';


export async function handler(
  event: APIGatewayProxyEvent & { body: string },
): Promise<APIGatewayProxyResult> {
    
  // Use event as an instance of MyLambdaEvent
  const myEvent: Observation= JSON.parse(event.body.data.dataSets[0].series.observations);


}

Run time validation

const Joi = require('joi');


const myLambdaEventSchema = Joi.object({
  observations: Joi.object().pattern(
    Joi.string(),
    Joi.array().items(Joi.number(), Joi.allow(null), Joi.number(), Joi.allow(null))
  ),
});




const { error, value } = myLambdaEventSchema.validate(dataToValidate);
