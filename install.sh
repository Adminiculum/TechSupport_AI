#!/bin/bash
# Ubuntu 24.04 Fresh Install Setup Script
# Run this to install everything needed for TechSupport_AI with Ollama + Docker

echo "=================================================="
echo "TechSupport_AI - Ubuntu 24.04 Setup Script"
echo "=================================================="
echo ""

# Update system
echo "[1/8] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip
echo ""
echo "[2/8] Installing Python 3 and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Install required Python packages
echo ""
echo "[3/8] Installing Python dependencies..."
pip3 install --break-system-packages streamlit requests pandas openpyxl python-dotenv

# Install Docker (official method)
echo ""
echo "[4/8] Installing Docker..."

# Remove old/conflicting Docker packages if any
echo "  → Removing old Docker packages (if any)..."
sudo apt remove -y $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc 2>/dev/null | cut -f1) 2>/dev/null || true

# Add Docker's official GPG key
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start and enable Docker
sudo systemctl enable docker
sudo systemctl start docker

# Allow current user to run Docker without sudo
sudo usermod -aG docker "$USER"
echo "  Docker installed. Note: Log out and back in for docker group to take effect."

# Install Ollama
echo ""
echo "[5/8] Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Wait a moment for installation to complete
sleep 2

# Start Ollama service
echo ""
echo "[6/8] Starting Ollama service..."
sudo systemctl enable ollama
sudo systemctl start ollama

# Wait for Ollama to start
sleep 3

# Pull recommended model
echo ""
echo "[7/8] Pulling llama3.2:3b model (this may take a few minutes)..."
ollama pull llama3.2:3b

# Set up project directory
echo ""
echo "[8/8] Setting up project structure..."
mkdir -p ~/TechSupport_AI/data

# Create a minimal setup_prompts.json if it doesn't exist
if [ ! -f ~/TechSupport_AI/data/setup_prompts.json ]; then
cat > ~/TechSupport_AI/data/setup_prompts.json <<'JSONEOF'
{
  "general": {
    "label": "General Assistant",
    "options": {
      "default": {
        "label": "Helpful Assistant",
        "value": "You are a helpful, friendly AI assistant."
      }
    }
  },
  "security": {
    "label": "Cybersecurity",
    "options": {
      "analyst": {
        "label": "Security Analyst",
        "value": "You are an expert cybersecurity analyst. Help the user understand vulnerabilities, CVEs, threat intelligence, and security best practices."
      },
      "cve": {
        "label": "CVE Researcher",
        "value": "You are a CVE researcher. Provide detailed, technical analysis of vulnerabilities including CVSS scores, affected systems, exploitation likelihood, and recommended mitigations."
      }
    }
  },
  "coding": {
    "label": "Coding Assistant",
    "options": {
      "default": {
        "label": "Code Helper",
        "value": "You are an expert software engineer. Help the user write clean, efficient, and well-documented code."
      }
    }
  }
}
JSONEOF
  echo "  Created default data/setup_prompts.json"
fi

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "Project structure created at: ~/TechSupport_AI/"
echo ""
echo "Next steps:"
echo "  1. Make sure your docker-compose.yml and app.py are in ~/TechSupport_AI/"
echo "  2. The app should already be starting via 'docker compose up --build' below."
echo ""
echo "To use OpenAI instead of Ollama:"
echo "  → Select 'OpenAI API' in the sidebar and paste your API key."
echo ""
echo "Useful commands:"
echo "  Check Ollama status : sudo systemctl status ollama"
echo "  List local models   : ollama list"
echo "  Pull a new model    : ollama pull mistral:7b"
echo "  Check Docker status : sudo systemctl status docker"
echo "  Docker version      : docker --version"
echo ""
echo "NOTE: Remember to log out and back in so your user can run Docker without sudo."
echo ""

# Launch the app
echo "=================================================="
echo "Launching TechSupport_AI with Docker Compose..."
echo "=================================================="
cd ~/TechSupport_AI
docker compose up --build
