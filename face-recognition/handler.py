import os
import boto3
from urllib.parse import unquote_plus
import logging
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
import cv2
import json
from PIL import Image, ImageDraw, ImageFont
from shutil import rmtree
import numpy as np
import torch


mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20) 
os.environ['TORCH_HOME'] = '/tmp'
resnet = InceptionResnetV1(pretrained='vggface2').eval() 

def face_recognition_function(key_path,data_path):
    
    img = cv2.imread(key_path, cv2.IMREAD_COLOR)
    boxes, _ = mtcnn.detect(img)

    
    key = os.path.splitext(os.path.basename(key_path))[0].split(".")[0]
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    face, prob = mtcnn(img, return_prob=True, save_path=None)
    saved_data = torch.load(data_path)  
    if face != None:
        emb = resnet(face.unsqueeze(0)).detach()  
        embedding_list = saved_data[0]  
        name_list = saved_data[1]  
        dist_list = []  
        for idx, emb_db in enumerate(embedding_list):
            dist = torch.dist(emb, emb_db).item()
            dist_list.append(dist)
        idx_min = dist_list.index(min(dist_list))

        
        with open("/tmp/" + key + ".txt", 'w+') as f:
            f.write(name_list[idx_min])
        return name_list[idx_min]
    else:
        print(f"No face is detected")
    return

def download_model(s3_client, bucket, object_key, download_path):
    """Download the model file if not present."""
    if not os.path.exists(download_path):
        logging.info(f"Downloading model file to {download_path}")
        s3_client.download_file(bucket, object_key, download_path)

def lambda_handler(event, context):
    print("IN LAMBDA HANDLER")
    s3_client = boto3.client("s3")
    model_bucket = "1229588726-face-data-pt"
    model_key = "data.pt"
    model_path = "/tmp/data.pt"
    bucket = event["bucket_name"]
    key = event["image_file_name"]
    
    
    download_model(s3_client, model_bucket, model_key, model_path)
    
    download_path = f"/tmp/{os.path.basename(key)}"
    output_file_path = f"/tmp/{os.path.splitext(os.path.basename(key))[0]}.txt"

    
    logging.info(f"Downloading {key} from {bucket}")
    s3_client.download_file(bucket, key, download_path)

    try:
        
        name = face_recognition_function(download_path, model_path)
        if name is not None:
            
            with open(output_file_path, 'w') as file:
                file.write(f"{name}\n")
            
            s3_client.upload_file(output_file_path, "1229588726-output", os.path.basename(output_file_path))
            logging.info(f"Uploaded results for {key}")
        else:
            logging.info(f"No face detected in {key}")
    except Exception as e:
        logging.error(f"Error processing file {key}: {e}")
    finally:
        
        if os.path.exists(download_path):
            os.remove(download_path)
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

    return {"statusCode": 200, "body": "Face recognition processed successfully"}


logging.basicConfig(level=logging.INFO)