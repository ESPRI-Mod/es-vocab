from fastapi import APIRouter, Request, HTTPException
import hmac
import hashlib
from es_vocab.utils.settings import SECRET_TOKEN

router = APIRouter(prefix="/webhook")
# Replace 'your-secret-token' with the actual secret token you entered in the GitHub webhook settings



def verify_signature(request_body: bytes, headers):
    # Extract the signature from the headers
    signature_256 = headers.get('X-Hub-Signature-256')
    
    if not signature_256:
        raise HTTPException(status_code=400, detail="Missing signature")

    # The signature will be of the format "sha256=..."
    sha_name, signature = signature_256.split('=')
    
    if sha_name != 'sha256':
        raise HTTPException(status_code=400, detail="Unsupported signature type")
    # Create a new HMAC digester using the secret token and SHA256
    mac = hmac.new(SECRET_TOKEN.encode(), msg=request_body, digestmod=hashlib.sha256)
    # Compare the signatures
    if not hmac.compare_digest(mac.hexdigest(), signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

@router.post("/repoupdate")
async def handle_webhook(request: Request):
    body = await request.body()
    
    # Verify the signature
    verify_signature(body, request.headers)
    
    return {"status": "success", "message": "Webhook received and verified"}
