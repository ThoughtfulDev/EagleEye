FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# 1. Install System Dependencies
RUN apt-get update && apt-get install -y \
    locales \
    git \
    curl \
    software-properties-common \
    unzip \
    wget \
    python3-pip \
    python3-dev \
    libboost-all-dev \
    build-essential \
    cmake \
    libffi-dev \
    firefox \
    dos2unix \
    # --- LIBRARIES TO FIX STATUS 1 ---
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libxt6 \
    libxrender1 \
    libasound2 \
    libnss3 \
    libxcomposite1 \
    xvfb \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

WORKDIR /EagleEye
COPY . /EagleEye

# Fix Windows line endings and permissions
RUN dos2unix /EagleEye/entry.sh && chmod +x /EagleEye/entry.sh

# Install Python Dependencies
RUN pip3 install --upgrade pip
RUN pip3 install "urllib3<2.0.0"
RUN pip3 install lxml_html_clean
RUN pip3 install -r requirements.txt

# Install Geckodriver (Updated for Firefox 147)
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.36.0-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver-v0.36.0-linux64.tar.gz

RUN mkdir -p /result

ENTRYPOINT ["/bin/bash", "/EagleEye/entry.sh"]