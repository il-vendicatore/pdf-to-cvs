FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y libtesseract-dev && \
    pip install -r requirements.txt

# Define environment variable for Access database connection
ENV ACCESS_DB_CONNECTION_STRING "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=/app/your_access_database.accdb;"

# Command to run your script
CMD ["python", "process_pdfs.py"]
