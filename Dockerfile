# Pull lightweight image of Python 3.14
FROM python:3.14-slim

# Create one working directory in docker /app
WORKDIR /app

# Copy dependencies to docker environment
COPY requirements.txt .

# Install dependencies in docker environment
RUN pip install -r requirements.txt

# Copy remaining files to docker
# Copy all the files from source and paste them to destination (/app)
COPY . . 

# Start the API server on PORT 8000
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

