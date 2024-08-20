import hashlib
import hmac
import json

from fastapi import APIRouter, HTTPException, Request, status

from es_vocab.utils.settings import SECRET_TOKEN

router = APIRouter(prefix="/webhook")
# Replace 'your-secret-token' with the actual secret token you entered in the GitHub webhook settings


def verify_signature(request_body: bytes, headers):
    # Extract the signature from the headers.
    signature_256 = headers.get("X-Hub-Signature-256")

    if not signature_256:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing signature")

    # The cryptographic signature must be SHA-256.
    sha_name, signature = signature_256.split("=")

    if sha_name != "sha256":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported signature type")
    # Create a new HMAC digester using the secret token and SHA-256.
    mac = hmac.new(SECRET_TOKEN.encode(), msg=request_body, digestmod=hashlib.sha256)
    # Compare the signatures.
    if not hmac.compare_digest(mac.hexdigest(), signature):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")


@router.post("/repoupdate", include_in_schema=False)
async def handle_webhook(request: Request):
    body = await request.body()

    # Verify the signature
    verify_signature(body, request.headers)

    # Verify branch main ? TODO: explicite this comment.
    payload = json.loads(body)
    if not payload.get("ref") == "refs/heads/main":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="push in main is not allowed")

    try:
        with open("/update/have_to_restart", "w") as f:
            f.write("1")

        return {"status": "success", "message": "Webhook received and verified"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Script failed with error: {str(e)}"
        )
