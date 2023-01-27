"""
Create an event handler for AWS Lambda that is triggered by a CloudWatch event for an ECS Task State Change.
Send a notification to a slack channel using the requests library.
"""

import requests

SLACK_CHANNEL = "#ecs-tasks"


def notify_slack(message):
    """Send the message to the slack channel."""
    requests.post(
        "https://hooks.slack.com/services/T0B9HF7N7/B0B9HF7N7/X9NQwY1wK0VjNjZ8RXjQm3W",
        data={"text": message},
    )
    
def lambda_handler(event, context):
    """
    Check the event type to make sure it is an ECS Task State Change
    If the lastStatus is FAILED then notify the channel.
    """
    if event['detail-type'] == 'ECS Task State Change':
        if event['detail']['lastStatus'] == 'FAILED':
            message = "ECS Task {} has failed".format(
                event['detail']['taskArn'])
            notify_slack(message)
