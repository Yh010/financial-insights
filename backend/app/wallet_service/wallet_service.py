import os
import uuid
import json
from google.auth import jwt, crypt
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv(dotenv_path="app/.env")

ISSUER_ID = os.getenv("WALLET_ISSUER_ID")
PASS_CLASS_SUFFIX = "receipt_pass_class"
SERVICE_ACCOUNT_FILE = "app/jwt/rasheed-466715-3cf75e00c9e8.json"
print(ISSUER_ID)

# def create_receipt_pass_jwt(receipt_data: dict) -> str | None:
#     """
#     Creates the final "Save to Google Wallet" JWT containing the pass object.
#     """
#     try:
#         pass_id = f"{ISSUER_ID}.{uuid.uuid4()}"
#         pass_class_id = f"{ISSUER_ID}.{PASS_CLASS_SUFFIX}"

#         # --- Define the Pass Object ---
#         pass_payload = {
#             'id': pass_id,
#             'classId': pass_class_id,
#             'genericType': 'GENERIC_TYPE_UNSPECIFIED',
#             'hexBackgroundColor': '#ffffff',
#             'logo': {
#                 'sourceUri': { 'uri': 'https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg' }
#             },
#             'cardTitle': { 'defaultValue': { 'language': 'en', 'value': 'Purchase Receipt' }},
#             'header': { 'defaultValue': { 'language': 'en', 'value': receipt_data.get("merchant_name", "Unknown Store") }},
#             'textModulesData': [
#                 {
#                     'header': 'Total Amount',
#                     'body': f"${float(receipt_data.get('total_amount', 0.0)):.2f}",
#                     'id': 'total'
#                 },
#                 {
#                     'header': 'Purchase Date',
#                     'body': receipt_data.get("purchase_date", "N/A"),
#                     'id': 'purchase_date'
#                 },
#                 {
#                     'header': 'Purchased Items',
#                     'body': "\n".join([
#                         f"{int(item.get('quantity', 1))}x {item.get('description', 'Item')} - ${float(item.get('price', 0.0)):.2f}"
#                         for item in receipt_data.get("items", [])
#                     ]),
#                     'id': 'items_list'
#                 }
#             ],
#             "linksModuleData": {
#                 "uris": [
#                     {
#                         "uri": f"https://your-agent-url.com/receipt/{pass_id}",
#                         "description": "Chat with Raseed Assistant",
#                     }
#                 ]
#             }
#         }

#         # --- Create the JWT Payload ---
#         creds = service_account.Credentials.from_service_account_file(
#             SERVICE_ACCOUNT_FILE,
#             scopes=['https://www.googleapis.com/auth/wallet_object.issuer']
#         )

#         claims = {
#             'iss': creds.service_account_email,
#             'aud': 'google',
#             'origins': ['http://localhost:3000', 'https://your-deployed-frontend-url.com'],
#             'typ': 'savetowallet',
#             'payload': { 'genericObjects': [ pass_payload ] }
#         }

#         signer = crypt.RSASigner.from_service_account_file(SERVICE_ACCOUNT_FILE)
#         signed_jwt = jwt.encode(signer, claims)

#         return signed_jwt.decode('utf-8')
#     except ValueError as e:
#         print(f"Error creating JWT (ValueError): {e}")
#         return None
#     except FileNotFoundError as e:
#         print(f"Error creating JWT (FileNotFoundError): Service account file not found: {e}")
#         return None
#     except Exception as e:
#         print(f"Error creating JWT (Unexpected error): {e}")
#         return None

def create_receipt_pass_jwt(receipt_data: dict) -> str | None:
    """
    Creates the final "Save to Google Wallet" JWT containing the pass object.
    """
    try:
        pass_id = f"{ISSUER_ID}.{uuid.uuid4()}"
        pass_class_id = f"{ISSUER_ID}.{PASS_CLASS_SUFFIX}"

        # --- Define the Pass Object ---
        pass_payload = {
            'id': pass_id,
            'classId': pass_class_id,
            'genericType': 'GENERIC_TYPE_UNSPECIFIED',
            'hexBackgroundColor': '#ffffff',
            'logo': {
                'sourceUri': { 'uri': 'https://storage.googleapis.com/wallet-lab-tools-codelab-artifacts-public/pass_google_logo.jpg' }
            },
            'cardTitle': { 'defaultValue': { 'language': 'en', 'value': 'Purchase Receipt' }},
            'header': { 'defaultValue': { 'language': 'en', 'value': receipt_data.get("merchant_name", "Unknown Store") }},
            'textModulesData': [
                {
                    'header': 'Total Amount',
                    'body': f"${float(receipt_data.get('total_amount', 0.0)):.2f}",  # CORRECTED
                    'id': 'total'
                },
                {
                    'header': 'Purchase Date',
                    'body': receipt_data.get("purchase_date", "N/A"),
                    'id': 'purchase_date'
                },
                {
                    'header': 'Purchased Items',
                    'body': "\n".join([
                        f"{int(item.get('quantity', 1))}x {item.get('description', 'Item')} - ${float(item.get('price', 0.0)):.2f}"  # CORRECTED
                        for item in receipt_data.get("items", [])
                    ]),
                    'id': 'items_list'
                }
            ],
            "linksModuleData": {
                "uris": [
                    {
                        "uri": f"https://your-agent-url.com/receipt/{pass_id}",
                        "description": "Chat with Raseed Assistant",
                    }
                ]
            }
        }

        # --- Create the JWT Payload ---
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer']
        )

        claims = {
            'iss': creds.service_account_email,
            'aud': 'google',
            'origins': ['http://localhost:3000', 'https://your-deployed-frontend-url.com'],
            'typ': 'savetowallet',
            'payload': { 'genericObjects': [ pass_payload ] }
        }

        signer = crypt.RSASigner.from_service_account_file(SERVICE_ACCOUNT_FILE)
        signed_jwt = jwt.encode(signer, claims)

        return signed_jwt.decode('utf-8')
    except ValueError as e:
        print(f"Error creating JWT (ValueError): {e}")
        return None
    except FileNotFoundError as e:
        print(f"Error creating JWT (FileNotFoundError): Service account file not found: {e}")
        return None
    except Exception as e:
        print(f"Error creating JWT (Unexpected error): {e}")
        return None

def get_save_to_wallet_url(signed_jwt: str) -> str:
    """Creates the final URL for the 'Add to Google Wallet' button."""
    return f"https://pay.google.com/gp/v/save/{signed_jwt}"

def generate_wallet_pass_link(receipt_data: dict) -> str :
    """
    Generates a complete 'Save to Google Wallet' link for a given receipt.

    This function acts as a tool for an agent. It takes a dictionary of
    receipt data, creates a signed JWT pass object, and returns the final
    URL that a user can click to save the pass.

    Args:
        receipt_data: A dictionary containing parsed receipt information.
    
    Returns:
        The 'Save to Google Wallet' URL as a string, or None if it fails.
    """
    print(f"Attempting to generate pass for: {receipt_data.get('merchant_name')}")
    
    # Create the signed JWT that represents the pass object
    signed_jwt = create_receipt_pass_jwt(receipt_data)

    if signed_jwt:
        # Get the final URL for the "Add to Google Wallet" button
        save_url = get_save_to_wallet_url(signed_jwt)
        print("✅ Successfully generated wallet save link.")
        return save_url
    else:
        print("❌ Failed to create the pass object JWT.")
        #return None
        return "Failed to create the pass object JWT."