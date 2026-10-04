import json
import re
import sys
from pathlib import Path

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet


ROOT = Path(__file__).parents[1]
text = (ROOT.parents[3] / "accounts.env").read_text()
key = re.search(r'^ACCOUNT_7_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', text, re.M).group(1).strip()
client = create_client(chain=studionet, account=create_account(account_private_key=key))
receipt = client.wait_for_transaction_receipt(
    transaction_hash=sys.argv[1],
    wait_until="finalized",
    retries=5,
    interval=1000,
    full_transaction=True,
)
leader = (receipt.get("consensus_data", {}).get("leader_receipt") or [{}])[0]
print(json.dumps({
    "status": receipt.get("status_name"),
    "consensus": receipt.get("result_name"),
    "execution": leader.get("execution_result"),
    "leader": leader,
}, default=str))
