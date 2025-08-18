# basemodel 

FROM python:3.12

LABEL maintainer="Basemodel Team"   

LABEL version="1.0"

LABEL description="Basemodel Docker image for running machine learning models."

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install dependencies
RUN pip3 install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000
# Command to run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
