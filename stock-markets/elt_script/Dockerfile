FROM python:3.13-slim

# Install PostgreSQL command-line tools
RUN apt-get update && apt-get install -y postgresql-client

# Copy requirements file
COPY requirements.txt .

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . .

# Set the default command to run the ELT script
CMD ["python", "elt_script.py"]