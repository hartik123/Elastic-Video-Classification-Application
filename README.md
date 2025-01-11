# AWS Lambda based Elastic Video Classification Application

## Overview

This project is an Image and Video Classification Cloud Application built using AWS services. It allows users to upload videos, which are processed and classified using a machine learning model. The architecture is designed to handle variable traffic with custom autoscaling capabilities, dynamically scaling between 0 to 20 instances based on demand. The system supports strong decoupling between video uploading and classification, ensuring scalability and efficiency.

## Architecture Diagram

![VideoClassificationArchitecture](https://github.com/user-attachments/assets/f6ec3311-b652-47db-bffc-607d7d77f1f6)

## Components
### 1. Users
   Multiple users (100+ concurrently) can upload videos containing images of persons for classification.
   The system efficiently handles varying traffic loads from different users.
2. AWS S3 Buckets (Storage)
   Three S3 buckets are used for storage:
   1. Input bucket: Stores uploaded videos, and triggers the video-splitting lambda function.
   2. Stage-1 bucket: Stores frames generated from the  Video Splitting Lambda Function.
3. AWS Lambda Function
   There are 2 lambda function
   1. Video-Splitting: This lambda function was created in python on the AWS cloud's website by using the library ffmpeg package to split videos into multiple frames and stores them in the intermediate bukcet called stage-1. The lambda function is automatically triggered on the uploading of a new video. Additionally, this function also invokes the face-recogniton lambda function.
   2. Face-Recognition: This lambda function was written in Python and was built after the creation of a  Docker images haviag all the face-recognition code ewith the libraries installed in it. The Docker image was uploaded to the Amazon Image Register. So, this function classifies the frames present in the stage-1 bucket and stores the output in the text format in the output bucket.


## Flow Summary

1. Users upload Videos for classification
2. Videos are stored in the input bucket and it triggers the video-splitting lambda function
3. Video-splitting lambda functions splits all video for which ot was triggered into multiple frames
4.  Video-splitting lambda function stores frames into stage-1 bucket and invokes/ccalls the face-recofnition lambda function
5.  face-recognition classifies the imag/frames conating a person, and stores the result in text format in output bucket.

## Key Features

Serverless Application: The application is developed using the AWS serverless computing power i.e. AWS Lambda with no handling of OS.
Autoscaling: The number of instances of the AWS Lambda function increases with the increase in number of uploads of a videos.
Strong Decoupling: The uploading of the video and the classification are separated using the S3 buckets, triggering, and the lambda function.
Persistent Storage: Amazon S3 provides durable storage for both input images and output results

## Technologies Used

AWS Lambda for serverless computing
AWS S3 (Simple Storage Service) for storing videos, frames and classification results.
AWS CloudWatch for monitoring funcstions.






