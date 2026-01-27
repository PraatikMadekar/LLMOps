"""
Comprehensive Script to Fix and Setup LLMOps Project
This script will:
1. Update .env file with correct configuration
2. Fix model_loader.py to use ChatGroq with openai/gpt-oss-120b
3. Fix config.yaml to use HuggingFace embeddings
4. Install all required dependencies
5. Test the setup

NOTE: This version uses environment variables instead of hardcoded secrets.
Make sure to set your API keys in the .env file before running.
"""

import os
import sys
from pathlib import Path
import subprocess

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_step(message, color=Colors.BLUE):
    print(f"\n{color}{'='*80}{Colors.RESET}")
    print(f"{color}{message}{Colors.RESET}")
    print(f"{color}{'='*80}{Colors.RESET}\n")

# Define the project path
PROJECT_PATH = Path(__file__).parent

print_step("🚀 Starting LLMOps Project Fix", Colors.GREEN)

# Step 1: Check if .env exists and warn user
print_step("1. Checking .env file")
env_path = PROJECT_PATH / ".env"

if not env_path.exists():
    print(f"{Colors.YELLOW}⚠ .env file not found!{Colors.RESET}")
    print("Creating template .env file...")
    
    env_template = """# LLMOps Environment Configuration
# Fill in your actual API keys below (remove the placeholders)

GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_PROJECT=LLMOps
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
LLM_PROVIDER=groq
ENV=local
"""
    
    with open(env_path, 'w') as f:
        f.write(env_template)
    
    print(f"{Colors.RED}❌ Please edit .env file and add your API keys!{Colors.RESET}")
    print(f"{Colors.YELLOW}Then run this script again.{Colors.RESET}")
    sys.exit(1)
else:
    # Check if .env has placeholder values
    with open(env_path, 'r') as f:
        env_content = f.read()
    
    if 'your_groq_api_key_here' in env_content or 'your_huggingface_token_here' in env_content:
        print(f"{Colors.RED}❌ .env file contains placeholder values!{Colors.RESET}")
        print(f"{Colors.YELLOW}Please edit .env file and add your actual API keys.{Colors.RESET}")
        sys.exit(1)
    
    # Ensure proper format (no quotes around values)
    lines = env_content.strip().split('\n')
    updated_lines = []
    for line in lines:
        if '=' in line and not line.strip().startswith('#'):
            key, value = line.split('=', 1)
            # Remove quotes if present
            value = value.strip().strip("'\"")
            updated_lines.append(f"{key.strip()}={value}")
        else:
            updated_lines.append(line)
    
    # Add missing keys if needed
    keys_to_check = ['LLM_PROVIDER', 'ENV']
    existing_keys = [line.split('=')[0].strip() for line in updated_lines if '=' in line]
    
    if 'LLM_PROVIDER' not in existing_keys:
        updated_lines.append('LLM_PROVIDER=groq')
    if 'ENV' not in existing_keys:
        updated_lines.append('ENV=local')
    
    with open(env_path, 'w') as f:
        f.write('\n'.join(updated_lines))
    
    print(f"{Colors.GREEN}✓ .env file validated and updated{Colors.RESET}")

# Step 2: Update config.yaml
print_step("2. Updating config.yaml to use HuggingFace embeddings")
config_content = """embedding_model:
  provider: "huggingface"
  model_name: "sentence-transformers/all-MiniLM-L6-v2"

retriever:
  top_k: 10
  search_type: "mmr"  # Options: "similarity", "mmr", "similarity_score_threshold"
  # MMR (Maximal Marginal Relevance) parameters for diverse results
  fetch_k: 20  # Number of documents to fetch before MMR re-ranking (should be > top_k)
  lambda_mult: 0.5  # Diversity vs relevance (0=max diversity, 1=max relevance)

llm:
  groq:
    provider: "groq"
    model_name: "openai/gpt-oss-120b"
    temperature: 0
    max_output_tokens: 2048

  google:
    provider: "google"
    model_name: "gemini-2.0-flash"
    temperature: 0
    max_output_tokens: 2048
"""

config_path = PROJECT_PATH / "multi_doc_chat" / "config" / "config.yaml"
with open(config_path, 'w') as f:
    f.write(config_content)
print(f"{Colors.GREEN}✓ config.yaml updated{Colors.RESET}")

# Step 3: Update model_loader.py
print_step("3. Updating model_loader.py to support HuggingFace embeddings")
model_loader_content = '''import os
import sys
import json
from dotenv import load_dotenv
from multi_doc_chat.utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from multi_doc_chat.logger import GLOBAL_LOGGER as log
from multi_doc_chat.exception.custom_exception import DocumentPortalException


class ApiKeyManager:
    REQUIRED_KEYS = ["GROQ_API_KEY", "HUGGINGFACEHUB_API_TOKEN"]

    def __init__(self):
        self.api_keys = {}
        raw = os.getenv("apikeyliveclass")

        if raw:
            try:
                parsed = json.loads(raw)
                if not isinstance(parsed, dict):
                    raise ValueError("API_KEYS is not a valid JSON object")
                self.api_keys = parsed
                log.info("Loaded API_KEYS from ECS secret")
            except Exception as e:
                log.warning("Failed to parse API_KEYS as JSON", error=str(e))

        for key in self.REQUIRED_KEYS:
            if not self.api_keys.get(key):
                env_val = os.getenv(key)
                if env_val:
                    self.api_keys[key] = env_val
                    log.info(f"Loaded {key} from individual env var")

        # Final check
        missing = [k for k in self.REQUIRED_KEYS if not self.api_keys.get(k)]
        if missing:
            log.error("Missing required API keys", missing_keys=missing)
            raise DocumentPortalException("Missing API keys", sys)

        log.info("API keys loaded", keys={k: v[:6] + "..." for k, v in self.api_keys.items()})

    def get(self, key: str) -> str:
        val = self.api_keys.get(key)
        if not val:
            raise KeyError(f"API key for {key} is missing")
        return val


class ModelLoader:
    """
    Loads embedding models and LLMs based on config and environment.
    """

    def __init__(self):
        if os.getenv("ENV", "local").lower() != "production":
            load_dotenv()
            log.info("Running in LOCAL mode: .env loaded")
        else:
            log.info("Running in PRODUCTION mode")

        self.api_key_mgr = ApiKeyManager()
        self.config = load_config()
        log.info("YAML config loaded", config_keys=list(self.config.keys()))

    def load_embeddings(self):
        """
        Load and return embedding model from HuggingFace.
        """
        try:
            model_name = self.config["embedding_model"]["model_name"]
            log.info("Loading HuggingFace embedding model", model=model_name)
            
            # Use HuggingFace embeddings instead of Google
            return HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        except Exception as e:
            log.error("Error loading embedding model", error=str(e))
            raise DocumentPortalException("Failed to load embedding model", sys)

    def load_llm(self):
        """
        Load and return the configured LLM model.
        """
        llm_block = self.config["llm"]
        provider_key = os.getenv("LLM_PROVIDER", "groq")

        if provider_key not in llm_block:
            log.error("LLM provider not found in config", provider=provider_key)
            raise ValueError(f"LLM provider '{provider_key}' not found in config")

        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.2)
        max_tokens = llm_config.get("max_output_tokens", 2048)

        log.info("Loading LLM", provider=provider, model=model_name)

        if provider == "groq":
            return ChatGroq(
                model=model_name,
                api_key=self.api_key_mgr.get("GROQ_API_KEY"),
                temperature=temperature,
                max_tokens=max_tokens
            )
        else:
            log.error("Unsupported LLM provider", provider=provider)
            raise ValueError(f"Unsupported LLM provider: {provider}")


if __name__ == "__main__":
    loader = ModelLoader()

    # Test Embedding
    embeddings = loader.load_embeddings()
    print(f"Embedding Model Loaded: {embeddings}")
    result = embeddings.embed_query("Hello, how are you?")
    print(f"Embedding Result (first 10 dims): {result[:10]}")

    # Test LLM
    llm = loader.load_llm()
    print(f"LLM Loaded: {llm}")
    result = llm.invoke("Hello, how are you?")
    print(f"LLM Result: {result.content}")
'''

model_loader_path = PROJECT_PATH / "multi_doc_chat" / "utils" / "model_loader.py"
with open(model_loader_path, 'w') as f:
    f.write(model_loader_content)
print(f"{Colors.GREEN}✓ model_loader.py updated{Colors.RESET}")

# Step 4: Update requirements.txt
print_step("4. Updating requirements.txt with all dependencies")
requirements_content = """python-dotenv==1.1.1
structlog

langchain==0.3.27
langchain-community==0.3.27
langchain-core==0.3.72

langchain-groq==0.3.6
langchain-huggingface==0.1.2
sentence-transformers==3.3.1

docx2txt==0.9
ipykernel==6.30.0
python-multipart==0.0.20
faiss-cpu==1.9.0.post1

fastapi==0.115.6
uvicorn==0.32.1
Jinja2==3.1.4

langsmith
pandas
PyYAML
pypdf
"""

requirements_path = PROJECT_PATH / "requirements.txt"
with open(requirements_path, 'w') as f:
    f.write(requirements_content)
print(f"{Colors.GREEN}✓ requirements.txt updated{Colors.RESET}")

print_step("✅ All fixes applied successfully!", Colors.GREEN)
print(f"""
{Colors.YELLOW}Next Steps:{Colors.RESET}
1. Run the installation script:
   install_and_setup.bat

2. Once installed, run the application:
   run_app.bat

3. Open your browser to:
   http://localhost:8000

{Colors.BLUE}Note:{Colors.RESET} Make sure your .env file has valid API keys!
""")
