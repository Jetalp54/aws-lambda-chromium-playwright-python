# AWS Lambda + Chromium + Playwright (Python)

This repository contains a **ready-to-use Docker image** for running
**Chromium + Playwright** inside **AWS Lambda** (Python), using the
Lambda Runtime Interface Client.

It is meant to be a clean base for automation / education case studies:
- Build container image locally (or in Cloud9).
- Push to ECR.
- Create a Lambda function using the image.
- Invoke the function to open a URL with Chromium and return metadata.

## Requirements

- AWS account (+ ECR + Lambda).
- Docker installed (locally or in Cloud9/EC2).
- AWS CLI v2 configured.
- Python 3.11+ (only if you want to run code locally outside Docker).

## 1. Install Playwright browsers (build-time)

From the repo root, run:

```bash
docker build -t lambda-chromium-playwright .
