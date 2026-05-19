import os
import logging

try:
    import boto3
    from botocore.exceptions import ClientError
except Exception:
    boto3 = None
    ClientError = Exception


def ensure_gcp_credentials():
    """Ensure GOOGLE_APPLICATION_CREDENTIALS is present.

    If the env var is already set, do nothing. Otherwise attempt to read the
    secret from AWS Secrets Manager and write it to /tmp/gcloud.json.
    This function is safe to call multiple times and is designed to be called
    lazily (only when Google Vision client is needed) to avoid cold-start
    overhead at process startup.
    """
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        return

    if boto3 is None:
        logging.warning('boto3 not available; cannot fetch GCP credentials.')
        return

    secret_name = os.environ.get("GCP_SECRET_NAME", "sbc-contentextraction-9cf6e2740a0d")
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    try:
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response.get('SecretString')
        if secret:
            target_path = os.path.join(os.environ.get('TMP_DIR', '/tmp'), 'gcloud.json')
            with open(target_path, 'w') as f:
                f.write(secret)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = target_path
            logging.info('GCP credentials written to %s', target_path)
        else:
            logging.warning('Secret %s did not contain a SecretString', secret_name)
    except ClientError as e:
        logging.warning('Could not retrieve secret %s: %s', secret_name, e)
    except Exception as e:
        logging.warning('Unexpected error while loading GCP credentials: %s', e)
