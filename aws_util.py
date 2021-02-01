import boto3
from botocore.exceptions import ClientError


def get_wait_parameters(**kwargs):
    return {
        k: v for k, v in kwargs.items() if k in (
            'StackName',
            'NextToken',
            'WaiterConfig'
        )
    }


def get_delete_stack_parameters(**kwargs):
    return {
        k: v for k, v in kwargs.items() if k in (
            'StackName',
            'RetainResources',
            'RoleARN',
            'ClientRequestToken'
        )
    }


def get_create_stack_parameters(**kwargs):
    return {
        k: v for k, v in kwargs.items() if k in (
            'StackName',
            'TemplateBody',
            'TemplateURL',
            'Parameters',
            'DisableRollback',
            'RollbackConfiguration',
            'TimeoutInMinutes',
            'NotificationARNs',
            'Capabilities',
            'ResourceTypes',
            'RoleARN',
            'OnFailure',
            'StackPolicyBody',
            'StackPolicyURL',
            'Tags',
            'ClientRequestToken',
            'EnableTerminationProtection'
        )
    }


def get_client():
    return boto3.client('cloudformation')


def create_stack(**kwargs):
    client = get_client()

    response = client.create_stack(**get_create_stack_parameters(**kwargs))

    if kwargs.get('wait', False):
        client.get_waiter('stack_create_complete').wait(**get_wait_parameters(**kwargs))

    return response


def delete_stack(**kwargs):
    client = get_client()

    response = client.delete_stack(**get_delete_stack_parameters(**kwargs))

    if kwargs.get('wait', False):
        client.get_waiter('stack_delete_complete').wait(**get_wait_parameters(**kwargs))

    return response


def stack_exists(stack_name: str) -> bool:
    try:
        boto3.client('cloudformation').describe_stacks(StackName=stack_name)
    except ClientError as error:
        return not f'Stack with id {stack_name} does not exist' == error.response.get('Error').get('Message')
    return True


def check_response(response: dict) -> bool:
    return 200 == response.get('ResponseMetadata').get('HTTPStatusCode')


def create_parameter_dict(parameters: dict) -> list:
    return [
        {
            'ParameterKey': k,
            'ParameterValue': str(v)
        } for k, v in parameters.items()
    ]


def create_tag_dict(tags: dict) -> list:
    return [
        {
            'Key': k,
            'Value': str(v)
        } for k, v in tags.items()
    ]
