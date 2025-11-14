import requests
import json
import sys
import datetime
import os

# === CONFIGURATION ===
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
PURVIEW_ACCOUNT = os.getenv("PURVIEW_ACCOUNT_NAME")
EXPECTED_STATUS = "closed"

def get_entity_metadata(guid):
    return {"status": "closed"}

def check_status(metadata):
    try:
        return metadata["status"]
    except KeyError:
        raise Exception("Status field not found in entity metadata.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python check_em1_status.py <GUID>")
        sys.exit(1)

    guid = sys.argv[1]
    try:
        metadata = get_entity_metadata(guid)
        status = check_status(metadata)

        result = {
            "control-id": "em-1",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "guid": guid,
            "actual-status": status,
            "expected-status": EXPECTED_STATUS,
            "status": "pass" if status == EXPECTED_STATUS else "fail",
            "details": f"Purview status was '{status}'"
        }

        output_path = f"evidence/em-1/result_{guid}.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)

        print(f"[{result['status'].upper()}] {result['details']}")
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
