# --- Builder Stage ---
FROM python:3.11-bookworm AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Runner Stage ---
FROM python:3.11-slim-bookworm AS runner

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user for Hugging Face security
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy installed packages and code
COPY --from=builder /install /usr/local
COPY --chown=user . .

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV NLTK_DATA=$HOME/app/nltk_data

# Pre-download NLTK data into the image
RUN python -m nltk.downloader -d $HOME/app/nltk_data punkt punkt_tab averaged_perceptron_tagger_eng wordnet omw-1.4 stopwords

# Hugging Face Spaces specifically use port 7860
EXPOSE 7860

# Start Uvicorn on 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]