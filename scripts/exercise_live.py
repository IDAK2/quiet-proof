import json
import re
import sys
import time
from pathlib import Path

from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet
from genlayer_py.contracts import actions as contract_actions


def studio_calldata(method=None, args=None, kwargs=None):
    value = {}
    if method is not None:
        value["method"] = method
    if args:
        value["args"] = args
    if kwargs:
        value["kwargs"] = kwargs
    return value


def finalized(client, tx):
    receipt = client.wait_for_transaction_receipt(
        transaction_hash=tx,
        wait_until="finalized",
        retries=180,
        interval=5000,
        full_transaction=True,
    )
    leader = (receipt.get("consensus_data", {}).get("leader_receipt") or [{}])[0]
    result = {"tx": str(tx), "consensus": receipt.get("result_name"), "execution": leader.get("execution_result")}
    print(json.dumps(result), flush=True)
    if result["execution"] != "SUCCESS" or result["consensus"] != "MAJORITY_AGREE":
        raise RuntimeError("StudioNet transaction did not reach successful validator agreement")


contract_actions.make_calldata_object = studio_calldata
ROOT = Path(__file__).parents[1]
text = (ROOT.parents[3] / "accounts.env").read_text()
key = re.search(r'^ACCOUNT_7_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)', text, re.M).group(1).strip()
client = create_client(chain=studionet, account=create_account(account_private_key=key))
address = sys.argv[1]
probe_id = "QP-CORE-20261004C"
due = int(time.time()) + 20
open_tx = client.write_contract(address=address, function_name="open_probe", args=[
    probe_id,
    "Current public operating condition of two independent developer infrastructure providers",
    "The provider explicitly reports an unresolved critical production outage on its status page",
    ["https://www.githubstatus.com/api/v2/status.json", "https://www.cloudflarestatus.com/api/v2/status.json"],
    due,
])
finalized(client, open_tx)
time.sleep(max(0, due - int(time.time()) + 2))
observe_tx = client.write_contract(address=address, function_name="observe", args=[probe_id])
finalized(client, observe_tx)
print(json.dumps(client.read_contract(address=address, function_name="get_probe", args=[probe_id]), default=str), flush=True)
