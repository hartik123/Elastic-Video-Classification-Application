import os
import subprocess
import boto3
from urllib.parse import unquote_plus
from botocore.exceptions import ClientError
import json
from constants import S3_NAME, INPUT_BUCKET_NAME, STAGE_1_BUCKET_NAME, FACE_RECOGNITION_LAMBDA_FUNC_NAME



s3_client = boto3.client("s3", region_name="us-east-1")
lambda_client = boto3.client('lambda')

def invoke_face_recognition(bucket_name, image_file_name):
    payload = {"bucket_name": bucket_name, "image_file_name": image_file_name}
    try:
        lambda_client.invoke(
            FunctionName=FACE_RECOGNITION_LAMBDA_FUNC_NAME,
            InvocationType="Event",
            Payload=json.dumps(payload)
        )
    except Exception as e:
        print(f"Error invoking face-recognition Lambda function: {str(e)}")

def lambda_handler(event, context):
    print("In the LAMBDA OF VIDEO SPLITTING")
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
        download_path = '/tmp/' + os.path.basename(key)
        outFile = '/tmp/' + os.path.splitext(os.path.basename(key))[0] + ".jpg"

        try:
            
            s3_client.download_file(bucket, key, download_path)

            
            command = [
                "/opt/bin/ffmpeg",
                "-i", download_path,
                "-vframes", "1",
                outFile
            ]
            
            
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(result.stdout)

            
            s3_client.upload_file(
                outFile,
                STAGE_1_BUCKET_NAME,
                os.path.basename(outFile)
            )
            invoke_face_recognition(STAGE_1_BUCKET_NAME, os.path.basename(outFile))
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error for file {key}: {e.output}")
        except Exception as e:
            
            print(f"Error processing file {key}: {str(e)}")
        finally:
            
            if os.path.exists(download_path):
                os.remove(download_path)
            if os.path.exists(outFile):
                os.remove(outFile)

    return {"statusCode": 200, "body": "Video processed successfully"}