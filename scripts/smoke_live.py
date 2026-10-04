import json
import re
import sys
import time
from pathlib import Path

from genlayer import create_account, create_client
from genlayer.chains import studionet


ROOT = Path(__file__).parents[1]
text = (ROOT.parents[3] / "accounts.env").read_text()
key = re.search(r'^ACCOUNT_7_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', text, re.M).group(1).strip()
client = create_client(chain=studionet, account=create_account(account_private_key=key))
address = sys.argv[1]
probe_id = "QP-LIVE-20261004"
args = [
    probe_id,
    "Public availability of two independent developer infrastructure status pages",
    "A source explicitly reports an unresolved critical outage affecting its public production service",
    ["https://www.githubstatus.com/", "https://www.cloudflarestatus.com/"],
    int(time.time()) + 3600,
]
tx = client.write_contract(address=address, function_name="open_probe", args=args)
print("open_probe_tx=" + str(tx), flush=True)
receipt = client.wait_for_transaction_receipt(
    transaction_hash=tx,
    wait_until="finalized",
    retries=180,
    interval=5000,
    full_transaction=True,
)
leader = (receipt.get("consensus_data", {}).get("leader_receipt") or [{}])[0]
print(json.dumps({
    "tx": str(tx),
    "consensus": receipt.get("result_name"),
    "execution": leader.get("execution_result"),
    "record": client.read_contract(address=address, function_name="get_probe", args=[probe_id]),
}, default=str), flush=True)
