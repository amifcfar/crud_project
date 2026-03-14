# 1. Use an official lightweight image
#FROM python:3.12-slim

# Create a non-root user and group
#RUN groupadd -r appuser && useradd -r -g appuser -m appuser

# 2. Set a working directory
#WORKDIR /home/appuser/app

# Copy all files from the current directory into the container
#COPY --chown=appuser:appuser . .

# Switch to the non-root user
#USER appuser

# 3. Copy dependency files first (cache layer)
#COPY requirements.txt .

# 4. Install dependencies securely
#RUN pip install --no-cache-dir -r requirements.txt

#RUN uvicorn main:app --reload

# 5. Copy app code
#COPY . .

# 6. Run as non-root user
#RUN useradd -m phoenix
#USER phoenix

# 7. Expose port and define entrypoint
#EXPOSE 8000
#CMD ["python3","/home/appuser/app/main.py"]

#CMD ["python3","main.app"]

FROM python:3.11-slim

WORKDIR /app

# 1. Copy only requirements first
COPY requirements.txt .

# 2. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of the code
COPY . .

RUN uvicorn main:app --reload

EXPOSE 8000

# 4. Run your app
CMD ["python", "main.py"]
