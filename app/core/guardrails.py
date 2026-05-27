import re

class Guardrails:
    """
    Topic filtering and guardrails layer to ensure the chatbot only
    answers technical questions.
    """
    
    ALLOWED_TOPICS = [
        "programming", "coding", "python", "javascript", "html", "css", "java", "c++", "go", "rust",
        "linux", "bash", "shell", "ubuntu", "centos", "debian",
        "docker", "container", "kubernetes", "k8s",
        "aws", "amazon web services", "ec2", "s3", "lambda", "cloud",
        "ai", "ml", "artificial intelligence", "machine learning", "neural network", "deep learning", "gemini",
        "devops", "ci/cd", "jenkins", "github actions", "gitlab", "terraform", "ansible",
        "cybersecurity", "infosec", "penetration testing", "cryptography", "malware",
        "data science", "data engineering", "big data", "hadoop", "spark", "pandas",
        "web development", "mobile development", "android", "ios", "react native", "flutter",
        "networking", "tcp", "ip", "dns", "load balancing", "firewall",
        "blockchain", "web3", "smart contracts", "ethereum",
        "game development", "unity", "unreal engine",
        "system administration", "sysadmin", "it support",
        "shukaku", "creator", "harshit", "agarwal",
        # Added 50+ new topics
        "agile", "scrum", "kanban", "software architecture", "microservices", "serverless", "cloud native",
        "google cloud", "gcp", "microsoft azure", "azure", "oracle cloud", "ibm cloud",
        "virtualization", "vmware", "virtualbox", "hyper-v",
        "version control", "git", "subversion", "mercurial",
        "continuous integration", "continuous deployment", "test driven development", "tdd", "bdd",
        "computer vision", "natural language processing", "generative ai", "large language models", "llm",
        "data mining", "data warehouse", "etl", "business intelligence",
        "information technology", "iot", "internet of things", "edge computing",
        "embedded systems", "arduino", "raspberry pi", "microcontroller",
        "quantum computing", "robotics", "automation",
        "cryptocurrency", "bitcoin", "solana", "nft", "defi",
        "quality assurance", "qa", "software testing", "user experience", "user interface"
    ]
    
    # Generic tech keywords for broader matches
    TECH_KEYWORDS = [
        "code", "script", "database", "sql", "nosql", "server", "api", "framework", 
        "backend", "frontend", "fullstack", "full stack", "deploy", "algorithm", "data structure",
        "bug", "error", "debug", "compile", "run", "variable", "function", "class",
        "architecture", "system", "infrastructure", "oop", "object oriented", "software engineering",
        "typescript", "php", "ruby", "kotlin", "swift", "scala", "perl", "lua", "c#",
        "react", "angular", "vue", "django", "flask", "spring", "express", "node.js", "laravel",
        "postgresql", "mysql", "mongodb", "redis", "cassandra", "sqlite", "oracle", "elasticsearch",
        "azure", "gcp", "digitalocean", "docker-compose", "git", "github", "gitlab", "bitbucket", "nginx", "apache",
        "pytorch", "tensorflow", "scikit-learn", "nlp", "cv", "openai", "llm", "prompt engineering",
        "memory leak", "recursion", "iteration", "polymorphism", "inheritance", "encapsulation", 
        "syntax", "interpreter", "threading", "concurrency", "async", "await", "promise", 
        "microservices", "restful", "graphql", "websocket", "json", "xml", "yaml", "regex",
        "tech", "technology", "stack", "web", "website", "app", "application", "software", "hardware",
        "computer", "program", "programming", "developer", "development", "engineer", "engineering",
        "ui", "ux", "interface", "design", "performance", "optimization", "security", "auth", "login",
        "network", "internet", "browser", "client", "p2p", "hosting", "domain", "dns", "http", "https",
        # Added 50+ new keywords
        "compiler", "runtime", "garbage collection", "memory management",
        "pointers", "references", "multithreading", "parallel processing", "synchronous", "asynchronous",
        "callback", "event loop", "state management", "props", "components", "hooks", "lifecycle",
        "dom", "virtual dom", "cssom", "responsive design", "accessibility", "a11y", "seo",
        "rest api", "soap", "rpc", "grpc", "webhooks", "payload", "endpoint", "middleware", "routing",
        "orm", "odm", "query language", "migrations", "indexing", "caching", "load balancer",
        "firewalls", "ssl", "tls", "certificates", "encryption", "decryption", "hashing", "salting",
        "authentication", "authorization", "oauth", "jwt", "saml", "sso",
        "containerization", "orchestration", "provisioning", "configuration management",
        "logging", "monitoring", "observability", "tracing", "metrics", "alerts"
    ]

    # Security related keywords that suggest prompt injection or jailbreaking
    UNSAFE_PATTERNS = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "ignore all directions",
        "disregard all previous",
        "bypass security",
        "bypass filters",
        "hack system",
        "reveal secrets",
        "show your api key",
        "print api key",
        "give me your api key",
        "reveal credentials",
        "database password",
        "show configuration",
        "private key",
        "auth token",
        "access token",
        "jailbreak",
        "you are now a",
        "pretend to be",
        "act as a",
        "forget all rules",
        "disregard the above",
        "system prompt",
        "system message",
        "developer mode",
        "god mode",
        "unrestricted",
        "without limits",
        "print your instructions",
        "what were your instructions",
        "your new instructions",
        "output your prompt",
        "disable safety",
        "override safety",
        "DAN mode",
        "do anything now",
        "you must now",
        "always output",
        "never refuse",
        "simulate",
        "hypothetical scenario",
        "say the following",
        "repeat after me"
    ]

    TOXIC_WORDS = [
        "idiot", "stupid", "dumb", "moron", "retard", "shut up", "fuck", "shit", "bitch", "asshole",
        "crap", "bastard", "dick", "cunt", "pussy", "slut", "whore", "fag", "faggot", "nigger", "nigga", 
        "twat", "wanker", "prick", "bullshit", "motherfucker", "cocksucker", "jackass", "douche", "douchebag",
        "kill yourself", "die", "suicide"
    ]

    def __init__(self):
        # Combine all valid topics into a single list
        self.all_keywords = set(self.ALLOWED_TOPICS + self.TECH_KEYWORDS)

    def is_safe_prompt(self, user_message: str) -> bool:
        """
        Check for common prompt injection or jailbreak patterns.
        """
        clean_msg = user_message.lower()
        for pattern in self.UNSAFE_PATTERNS:
            if pattern in clean_msg:
                return False
        return True
        
    def is_toxic(self, user_message: str) -> bool:
        """
        Check for profanity or toxic language.
        """
        clean_msg = user_message.lower()
        for word in self.TOXIC_WORDS:
            if re.search(r'\b' + re.escape(word) + r'\b', clean_msg):
                return True
        return False

    def is_technical_query(self, user_message: str) -> bool:
        """
        Check if the user message relates to allowed technical topics.
        """
        # Clean the message and convert to lowercase for matching
        clean_msg = user_message.lower()
        
        # If it's a very short greeting, we can let it pass to the model 
        # so it can respond professionally.
        greetings = ["hi", "hello", "hey", "who are you", "help"]
        if clean_msg.strip() in greetings or len(clean_msg) < 15:
            return True
            
        # Check for keyword matches
        for keyword in self.all_keywords:
            # For keywords with special chars (like c++, ci/cd), simple substring matching avoids regex boundary bugs
            if not keyword.isalnum():
                if keyword in clean_msg:
                    return True
            # For regular words, use regex to avoid partial matches (e.g., 'go' in 'good')
            elif re.search(r'\b' + re.escape(keyword) + r'\b', clean_msg):
                return True
                
        return False
        
    def check_message(self, user_message: str) -> dict:
        """
        Checks input length, toxicity, security guardrails, and topic relevance.
        Returns a dict with 'is_valid' and an optional 'rejection_message'.
        """
        # 1. Length Check (Max 1000 chars)
        if len(user_message) > 1000:
            return {
                "is_valid": False,
                "rejection_message": {
                    "response": "Your message is too long. Please limit prompts to 1000 characters or less.",
                    "code_snippet": None,
                    "status": "error"
                }
            }
            
        # 2. Toxicity Check
        if self.is_toxic(user_message):
            return {
                "is_valid": False,
                "rejection_message": {
                    "response": "Your message contains inappropriate language. Please maintain a professional tone.",
                    "code_snippet": None,
                    "status": "error"
                }
            }
            
        # 3. Security Check
        if not self.is_safe_prompt(user_message):
            return {
                "is_valid": False,
                "rejection_message": {
                    "response": "Security Alert: Your prompt contains unsafe patterns or attempts to bypass system instructions. Request blocked.",
                    "code_snippet": None,
                    "status": "error"
                }
            }
            
        # 4. Topic Check
        if not self.is_technical_query(user_message):
            return {
                "is_valid": False,
                "rejection_message": {
                    "response": "I am not here to help you with this, Please ask me some technical questions.",
                    "code_snippet": None,
                    "status": "rejected"
                }
            }
            
        return {"is_valid": True}
