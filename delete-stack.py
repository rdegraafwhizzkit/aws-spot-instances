from dynaconf import Dynaconf
from aws_util import delete_stack
from pprint import pprint as pp

settings = Dynaconf(
    env='dt',
    settings_files=['settings.yaml'],
    environments=True
)

pp(delete_stack(
    wait=True,
    StackName=settings.stack_name
))
