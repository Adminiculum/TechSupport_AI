 Cybersecurity TechSupport AI / CyberOLLAMA

Intelligent AI Chat Interface for Technical Support and Cybersecurity

A powerful, customizable AI chatbot interface for cybersecurity professionals, developers, and IT support teams. 100% local with Ollama or cloud-based with OpenAI — complete privacy when you need it, flexibility when you want it.


 Key Features

 100% Local and Private
Run completely offline with Ollama - no API keys, no data leaving your infrastructure. Air-gapped capable for secure environments. Complete privacy for sensitive cybersecurity operations.

 Cybersecurity and IT Focus
Pre-configured for security professionals including pentesting, DFIR, threat intelligence, and vulnerability analysis. Over 13 specialized IT roles including Service Desk, Network Admin, DBA, Cloud Engineer, and Security Officer. Technical response format with exact CLI commands, event IDs, log patterns, and resolution paths. Production-ready syntax for PowerShell, Bash, Python, SQL, and Terraform.

 Enterprise-Grade Features
Multi-provider support for Ollama local and OpenAI API with all GPT versions. Fine-tuning controls for temperature, Top P, Max Tokens, presence and frequency penalties. Streaming output with real-time responses and typing animation. Knowledge cutoff to simulate model knowledge limitations. Session management with persistent chat sessions and unique IDs.

 Multiple Local Models
Support for all Ollama models including Phi-3 Mini, Llama 3.2, Mistral, Gemma, and CodeLlama. Instant switching between models. Pull any model from Ollama library.


 Quick Start Guide

 Prerequisites
Ubuntu 24.04 or any Debian-based distribution. Docker optional for containerized deployment. Ollama for local models.

 Method 1: Automatic Installation (Ubuntu 24.04)

mkdir -p ~/TechSupport_AI
cd ~/TechSupport_AI
chmod +x install.sh
./install.sh

The script updates system packages, installs Python 3, pip, and dependencies, installs Docker and Docker Compose, installs Ollama and pulls the default model llama3.2:3b, sets up the project structure, and launches the application.

 Method 2: Manual Installation

pip install streamlit requests pandas openpyxl python-dotenv
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
ollama pull phi3:mini
cd ~/TechSupport_AI/app
streamlit run app.py

 Method 3: Docker Compose

cd ~/TechSupport_AI
docker compose up --build

In another terminal, pull models:
ollama pull phi3:mini
ollama pull llama3.2:3b

Access the application at http://localhost:8501


 Pre-configured IT and Cybersecurity Roles

Service Desk Manager - Tier 3: Root cause plus event ID plus specific fix plus KB reference

Desktop Support Engineer: Diagnostic command plus expected output plus remediation script

Network Administrator CCIE: Show command with filters plus error pattern plus config change plus rollback

Systems Administrator: Log entry plus event ID plus one-liner fix plus verification command

Database Administrator DBA: Performance query plus thresholds plus index change plus rollback

IT Project Manager: Critical path plus resource impact plus risk mitigation plus stakeholder update

IT Asset Manager: Compliance gap plus cost exposure plus reconciliation script plus negotiation position

Cloud Engineer: Misconfiguration plus CIS ID plus Terraform code plus cost impact plus monitoring alert

DevOps Engineer: Pipeline error plus debug command plus YAML fix plus validation

IT Vendor Manager: Contract clause plus SLA breach plus service credit plus leverage point

IT Security Officer GRC: Control gap plus policy section plus technical implementation plus exception process

Backup Administrator: Backup error plus RPO or RTO impact plus recovery command plus validation

IT Compliance Auditor: Control objective plus evidence required plus sampling plus deficiency rating

Security Analyst: CVE analysis plus CVSS score plus exploit likelihood plus mitigation

CVE Researcher: Technical analysis plus affected systems plus exploitation plus mitigations


 Configuration Files

docker-compose.yml configures the Docker container with host network mode for Ollama access, mounting the app and data directories.

install.sh is an automated Ubuntu setup script that installs all dependencies and launches the application.

app.py is the main application with Streamlit UI components, Ollama and OpenAI API integration, chat history management, parameter controls, and streaming response handling.

style.css provides custom modern styling with dark theme sidebar, green accent colors, responsive design, custom animations, and terminal-like status bar.

setup_prompts.json contains JSON configuration for all IT roles with labels and system messages.

config.toml configures Streamlit server settings including CORS and XSRF protection.


 Advanced Configuration

 Adding Custom Models with Ollama
ollama pull mistral:7b
ollama pull codellama:7b
ollama pull gemma2:2b
ollama pull dolphin-mistral:7b

 Custom Role Creation
Edit data/setup_prompts.json to add your own roles:

{
  "your_custom_role": {
    "label": "Your Role Display Name",
    "value": "You are a role with expertise. Answer with format. Maximum constraints."
  }
}

 Environment Variables
Create .env in the app directory:
OPENAI_API_KEY=sk-your-key-here
OLLAMA_HOST=http://localhost:11434


 Security Considerations

The 100% local option ensures no data ever leaves your machine when using Ollama. API keys are stored only in session state and never persisted to disk. Session isolation with unique session IDs prevents chat history leakage. The system is air-gap capable and can run completely offline in secure environments. There is no telemetry, tracking, analytics, or phone home functionality.


 Troubleshooting

 Ollama Connection Issues
sudo systemctl status ollama
sudo systemctl restart ollama
curl http://localhost:11434/api/tags

 Docker Permissions
sudo usermod -aG docker $USER
Log out and back in

 Model Not Responding
ollama list
ollama pull llama3.2:3b

 Streamlit Port Conflict
streamlit run app.py --server.port=8502

 No Models Showing in Dropdown
curl http://localhost:11434/api/tags
ollama pull phi3:mini


 Performance Optimization

For production deployment, use Docker with resource limits. For development, run directly with Python for faster iteration. For memory constraints, use smaller models like phi3:mini or llama3.2:1b. When GPU is available, Ollama automatically uses GPU acceleration. For multi-user environments, deploy behind a reverse proxy with authentication.

 Roadmap

Multi-user support with role-based access control
Chat history export to PDF, Markdown, and JSON
RAG integration for custom knowledge bases
Plugin system for custom tools and integrations
Team collaboration with shared sessions
API endpoint for external integration
Mobile app for on-the-go access
Voice input for hands-free operation


 Contributing

Contributions are welcome. Fork the repository, create your feature branch, commit your changes, push to the branch, and open a Pull Request. Maintain the cybersecurity and IT focus. Keep responses technical and production-ready. Add tests for new features and update documentation.


 License

This project is licensed under the MIT License. See the LICENSE file for details.


 Acknowledgments

Streamlit for the web framework, Ollama for local model inference, OpenAI for API compatibility, and all contributors and testers.


 Support and Community

GitHub Issues for bug reports and feature requests
Documentation Wiki and guides
Email for maintainer contact


 Use Cases

Cybersecurity: Threat analysis, pentesting assistance, incident response
IT Support: Tier 3 escalation, root cause analysis, knowledge base creation
DevOps: Pipeline debugging, infrastructure as code, monitoring setup
Cloud Engineering: Terraform generation, cost optimization, security compliance
Database Administration: Query optimization, performance tuning, backup strategies
Compliance: Audit preparation, control testing, evidence collection


 Quick Commands Reference

cd ~/TechSupport_AI/app && streamlit run app.py
cd ~/TechSupport_AI && docker compose up
ollama pull dolphin-mistral:7b
ollama list
journalctl -u ollama -f


Cybersecurity TechSupport AI / CyberOLLAMA - Your intelligent, private AI assistant for cybersecurity and IT operations.
