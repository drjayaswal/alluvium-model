# --- Stage 1: Builder ---
# We use a full image to compile/install dependencies
FROM python:3.11-bookworm AS builder

WORKDIR /app

# Install build dependencies if any C-extensions are needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies to a temporary folder
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# --- Stage 2: Runner ---
# We use a slim image for the final production environment
FROM python:3.11-slim-bookworm AS runner

# Install runtime-only system dependencies (libgomp1 is required for many ML libs like scikit-learn/spacy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the installed python packages from the builder
COPY --from=builder /install /usr/local

# Copy the rest of your application code
COPY . .

# --- Environment Variables ---
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set the NLTK data path so the app knows where to look
ENV NLTK_DATA=/app/nltk_data

# --- Pre-download NLTK Data ---
# This ensures the "Cold Start" is fast because the data is already in the image
RUN python -m nltk.downloader -d /app/nltk_data punkt punkt_tab averaged_perceptron_tagger_eng wordnet omw-1.4 stopwords

# Render uses the PORT environment variable
EXPOSE 10000

# Use a shell form to allow the $PORT variable to be substituted correctly
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]