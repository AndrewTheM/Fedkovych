#!/bin/bash

# Update the package list
echo "Updating package list..."
sudo apt update

# Install ffmpeg
echo "Installing ffmpeg..."
sudo apt install -y ffmpeg

# Verify the installation
echo "Verifying ffmpeg installation..."
ffmpeg -version

echo "ffmpeg installation complete!"