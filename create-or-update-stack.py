from dynaconf import Dynaconf
from pprint import pprint as pp
from datetime import datetime, timedelta
from requests import get
import base64
from aws_util import create_stack_or_change_set, create_parameter_dict, create_tag_dict

settings = Dynaconf(
    env='dt',
    settings_files=['settings.yaml'],
    environments=True
)

parameters = create_parameter_dict(settings.parameters)
tags = create_tag_dict(settings.get('tags', {}))

parameters.extend([
    {
        'ParameterKey': 'ValidUntil',
        'ParameterValue': (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    },
    {
        'ParameterKey': 'HomeIp',
        'ParameterValue': '{}/32'.format(get('https://api.ipify.org').text)
    }
])

user_data = settings.parameters.get('UserData', '')

if '' != user_data:
    with open(user_data, 'r') as f:
        user_data = ''.join(f.readlines())
    parameters.extend([
        {
            'ParameterKey': 'UserData',
            'ParameterValue': base64.b64encode(user_data.encode('UTF-8')).decode('UTF-8')
        }
    ])

with open(settings.template_file, 'r') as f:
    template_body = ''.join(f.readlines())
    pp(create_stack_or_change_set(
        StackName=settings.stack_name,
        Parameters=parameters,
        TemplateBody=template_body,
        Tags=tags,
        wait=True
    ))
