FROM python:3.11-bookworm

RUN apt-get update -y && apt-get upgrade -y

RUN pip3 install --upgrade pip
RUN pip3 install uv

COPY ./requirements.txt /seo-analyzer/

RUN uv pip install --system --verbose --requirement /seo-analyzer/requirements.txt
RUN uv cache clean --verbose

COPY . /seo-analyzer

# Create a non-root user
RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser

# Set ownership of the app directory
RUN chown -R appuser:appgroup /seo-analyzer

# Create data and reports directories
RUN mkdir -p /app/data /app/reports && chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

WORKDIR /seo-analyzer

# Expose port for Streamlit dashboard
EXPOSE 8501

# Default to running the dashboard
ENTRYPOINT ["python", "main.py"]
CMD ["dashboard"]
