FROM python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy requirements first and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the application including model file
COPY . .

# Streamlit port & entry
ENV PORT=8080
EXPOSE 8080

# CMD: pass ENV properly
CMD ["streamlit", "run", "streamlit_otomoto.py", "--server.port=8080", "--server.address=0.0.0.0"]
