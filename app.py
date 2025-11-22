import os
import logging
from flask import Flask, render_template, request, jsonify

# --- CONFIGURATION ---
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key_for_testing_only")

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AEGIS_GUARD")

# --- AEGIS GUARD (Security Layer) ---
class AegisGuard:
    """
    Middleware to simulate high-level security checks.
    In a real scenario, this would handle encryption, IP whitelisting, and threat detection.
    """
    @staticmethod
    def scan_request(req):
        client_ip = req.remote_addr
        user_agent = req.headers.get('User-Agent')
        
        # Simulation of security screening
        if not user_agent:
            logger.warning(f"Security Alert: Suspicious request from {client_ip}")
            return False
        
        logger.info(f"Aegis Guard: Request from {client_ip} scanned and cleared.")
        return True

# --- PAPI (Intelligence Layer) ---
class PAPI_AI:
    """
    The Personal Intelligence Logic.
    Responses change based on the Subscription Tier.
    """
    def __init__(self):
        self.name = "PAPI"
    
    def generate_response(self, message, tier):
        message = message.lower()
        
        if tier == 'free':
            return f"[Free Tier]: I can help with that basics. {self._basic_logic(message)}"
        elif tier == 'standard':
            return f"[Standard]: Let's dig a bit deeper. {self._standard_logic(message)}"
        elif tier == 'pro':
            return f"[PRO - Aegis Protected]: precise analysis initiated. {self._pro_logic(message)}"
        else:
            return "Error: Invalid subscription tier."

    def _basic_logic(self, msg):
        if "hello" in msg: return "Hi there. I am PAPI."
        return "I am listening. Please upgrade for advanced advice."

    def _standard_logic(self, msg):
        if "plan" in msg: return "I have generated a schedule for you."
        return "I am processing your request with standard priority."

    def _pro_logic(self, msg):
        # Simulating high-level executive function
        return f"Processing '{msg}' with advanced heuristics. Optimization strategy ready."

# Initialize AI
papi = PAPI_AI()

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # 1. Security Check
    if not AegisGuard.scan_request(request):
        return jsonify({"response": "AEGIS GUARD: Connection Blocked due to security protocol."}), 403

    # 2. Process Input
    data = request.json
    user_message = data.get('message', '')
    user_tier = data.get('tier', 'free')

    if not user_message:
        return jsonify({"response": "Please say something."})

    # 3. Generate Response
    ai_response = papi.generate_response(user_message, user_tier)
    
    return jsonify({"response": ai_response})

@app.route('/health')
def health_check():
    return "System Operational", 200

if __name__ == '__main__':
    # Run locally
    app.run(debug=True, port=5000)
