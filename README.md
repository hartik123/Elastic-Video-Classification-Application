# AWS Lambda-Based Elastic Video Classification Application

## Overview
This project is an **Image and Video Classification Cloud Application** built using AWS services. It allows users to upload videos, which are processed and classified using a machine learning model. The architecture is designed to handle variable traffic with custom autoscaling capabilities, dynamically scaling between 0 to 20 instances based on demand. The system supports strong decoupling between video uploading and classification, ensuring scalability and efficiency.

## Architecture Diagram
![Video Classification Architecture](https://github.com/user-attachments/assets/f6ec3311-b652-47db-bffc-607d7d77f1f6)

## Features
- **Serverless Architecture**: Built entirely using AWS Lambda, removing the need for managing servers or operating systems.
- **Autoscaling**: Automatically scales the number of Lambda instances based on the volume of video uploads.
- **Strong Decoupling**: Video uploading and classification are decoupled using S3 buckets and Lambda triggers.
- **Persistent Storage**: Durable storage for videos, frames, and classification results using Amazon S3.

## Components
### 1. Users
- Multiple users (100+ concurrently) can upload videos containing images of persons for classification.
- The system efficiently handles varying traffic loads from different users.

### 2. AWS S3 Buckets (Storage)
Three S3 buckets are used for storage:
1. **Input Bucket**: Stores uploaded videos and triggers the video-splitting Lambda function.
2. **Stage-1 Bucket**: Stores frames generated by the video-splitting Lambda function.
3. **Output Bucket**: Stores classification results in text format.

### 3. AWS Lambda Functions
1. **Video-Splitting Function**:
   - Written in Python, created using the `ffmpeg` library.
   - Splits videos into frames and stores them in the Stage-1 bucket.
   - Automatically triggered upon video uploads to the input bucket.
   - Invokes the face-recognition Lambda function for further processing.

2. **Face-Recognition Function**:
   - Written in Python and packaged as a Docker image.
   - Docker image is stored in Amazon Elastic Container Registry (ECR).
   - Processes frames from the Stage-1 bucket using the MTCNN model to classify images containing persons.
   - Outputs results in text format, stored in the output bucket.

## Workflow
1. Users upload videos to the **Input Bucket**.
2. The **Input Bucket** triggers the video-splitting Lambda function.
3. The video-splitting function:
   - Splits the uploaded videos into frames.
   - Stores frames in the **Stage-1 Bucket**.
   - Invokes the face-recognition Lambda function.
4. The face-recognition function:
   - Processes frames from the **Stage-1 Bucket**.
   - Classifies images containing persons.
   - Stores classification results as text in the **Output Bucket**.

## Technologies Used
- **AWS Lambda**: For serverless computing.
- **AWS S3**: For storing videos, frames, and classification results.
- **AWS CloudWatch**: For monitoring Lambda function executions and performance.

## Getting Started
### Prerequisites
- AWS account with access to S3, Lambda, and ECR.
- Docker installed locally for building the face-recognition image.

### Installation
1. Clone this repository.
2. Deploy the Lambda functions and create the required S3 buckets.
3. Build and push the Docker image for the face-recognition function to Amazon ECR.
4. Set up triggers for S3 buckets to invoke the respective Lambda functions.

### Usage
- Upload videos to the Input Bucket to trigger the classification pipeline.
- Monitor the results in the Output Bucket.


