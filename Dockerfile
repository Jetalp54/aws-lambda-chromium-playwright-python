# =============================================================
# 1. Build Stage (install dependencies, copy source files)
# =============================================================
FROM mcr.microsoft.com/playwright/python:v1.47.0-noble AS build

# Working directory for the app
WORKDIR /app

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src


# =============================================================
# 2. Runtime Stage (actual Lambda image)
# =============================================================
FROM mcr.microsoft.com/playwright/python:v1.47.0-noble

# Install AWS Lambda runtime interface client so this image
# runs natively as a Lambda container image.
RUN pip install --no-cache-dir awslambdaric

# Working directory for Lambda
WORKDIR /var/task

# Copy everything from the build stage
COPY --from=build /app /var/task

# AWS Lambda entrypoint
ENTRYPOINT [ "python", "-m", "awslambdaric" ]

# AWS Lambda handler path (module.function)
CMD [ "src.handler.lambda_handler" ]
