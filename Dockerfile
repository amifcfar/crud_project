# 1. Use an official lightweight image
FROM python:3.12-slim

# 2. Set a working directory
WORKDIR /app

# 3. Copy dependency files first (cache layer)
COPY requirements.txt .

# 4. Install dependencies securely
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy app code
COPY app/ .

# 6. Run as non-root user
RUN useradd -m myuser
USER myuser

# 7. Expose port and define entrypoint
EXPOSE 8000
CMD ["python", "main.py"]