# 🧱 Base image with Python installed
FROM python:3.9-slim

# 📁 Set the working directory inside the container
WORKDIR /app

# 🧹 Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# 🖥️ Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# 📦 Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 📥 Copy your app code into the container
COPY . .

# 🚪 Expose the port Flask will run on
EXPOSE 5000

# 🚀 Start the Flask app
CMD ["python", "run.py"]
