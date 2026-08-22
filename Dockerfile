# =====================================================================
# 1. BASE SYSTEM LAYER
# =====================================================================
# Use the official, minimal Python footprint built on Debian Buster slim
FROM python:3.10-slim

# Prevent Python from writing .pyc files to disk (saves container space)
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent Python from buffering stdout/stderr (ensures live, instant logging in Render)
ENV PYTHONUNBUFFERED=1

# =====================================================================
# 2. DEPENDENCY & ENVIRONMENT BUILD LAYER
# =====================================================================
# Establish an isolated internal application workspace
WORKDIR /workspace

# Install system-level dependencies required for compiling heavy math operations safely
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the dependency sheet first to isolate and utilize Docker caching
COPY requirements.txt .

# Install Python modules without storing local cache data to optimize container size
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =====================================================================
# 3. CODE ENCAPSULATION LAYER
# =====================================================================
# Copy all engine code and asset files into the workspace
COPY . .

# Expose the precise port that the internal framework listens on
EXPOSE 8501

# Add standard web status health checks to make the deployment production-grade
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# =====================================================================
# 4. EXECUTION RUNTIME ENGINE
# =====================================================================
# Start the Streamlit server bound to global interfaces and explicit port
# Disables clean-up prompts and overrides CORS for smooth Render routing
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]
