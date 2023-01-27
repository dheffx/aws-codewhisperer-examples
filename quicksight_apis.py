import boto3
import json
import logging

# init python logger
log = logging.getLogger()


def describe_analysis(quicksight_client, aws_account_id, analysis_id):
    """Describe a Quicksight Analysis Definition"""
    try:
        response = quicksight_client.describe_analysis_definition(
            AwsAccountId=aws_account_id,
            AnalysisId=analysis_id
        )
    except Exception as e:
        log.error(e)
        raise e

    # Return the Definition key in the response
    return response['Analysis']


def save_definition(definition, filename):
    """Convert the definition object to JSON and save to file"""
    # Convert the JSON object to a string
    definition_string = definition.to_json()

    # Save the string to a file
    with open(filename, 'w') as f:
        f.write(definition_string)


def create_analysis(quicksight_client, aws_account_id, filename, analysis_name):
    """
        1. Read the contents of the file and parse its JSON
        2. Create an analysis_id that is a combination of analysis_name and the definition's AnalysisId
        3. Create the analysis using the analysis_id and definition
        4. Return the analysis_id
    """
    # Read the file contents
    with open(filename, 'r') as f:
        definition = json.load(f)

    # Create a unique analysis_id
    analysis_id = analysis_name + '_' + definition["AnalysisId"]

    # Create the analysis
    try:
        response = quicksight_client.create_analysis(
            AwsAccountId=aws_account_id,
            AnalysisId=analysis_id,
            Name=analysis_name,
            AnalysisSourceEntity=definition.to_json()
        )
    except Exception as e:
        log.error(e)
        raise e

    # Return the analysis_id
    return response['AnalysisId']





def main():
    """
    1. Describe the definition of a Quicksight Analysis by its ID
    2. Save the output as a file
    3. Create new Quicksight Analysis using the file's definition as an input
    """

    quicksight_client = boto3.client("quicksight")
    aws_account_id = "1234567890"
    analysis_id = "9876543210"
    filename = "analysis_definition.json"
    definition = describe_analysis(
        quicksight_client, aws_account_id, analysis_id)
    save_definition(definition, filename)
    create_analysis(quicksight_client, aws_account_id,
                    filename, "New Analysis")
