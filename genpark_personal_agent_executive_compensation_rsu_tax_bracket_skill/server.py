# -*- coding: utf-8 -*-
"""MCP Server for Executive Compensation RSU & Equity Tax Bracket Copilot Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import ExecutiveCompensationRSUTaxOptimizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "audit_rsu_vesting_tax_deficit",
        "description": "Audit upcoming RSU vests for statutory 22% supplemental withholding shortfall against actual 37% marginal federal tax bracket.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "annual_base_salary_usd": {
                    "type": "number"
                },
                "rsu_vest_value_usd": {
                    "type": "number"
                },
                "statutory_withholding_rate_pct": {
                    "type": "number",
                    "description": "Default 22.0% for equity under $1M"
                },
                "effective_marginal_tax_bracket_pct": {
                    "type": "number",
                    "description": "e.g. 37.0% for top federal bracket"
                },
                "state_tax_rate_pct": {
                    "type": "number",
                    "description": "e.g. 9.3% in CA"
                }
            },
            "required": [
                "annual_base_salary_usd",
                "rsu_vest_value_usd"
            ]
        }
    },
    {
        "name": "synthesize_quarterly_estimated_tax_plan",
        "description": "Synthesize IRS Form 1040-ES quarterly estimated tax voucher allocations to eliminate underpayment penalty (IRC 6654).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "total_tax_underwithheld_usd": {
                    "type": "number"
                },
                "prior_year_total_tax_liability_usd": {
                    "type": "number"
                },
                "current_projected_liability_usd": {
                    "type": "number"
                }
            },
            "required": [
                "total_tax_underwithheld_usd",
                "prior_year_total_tax_liability_usd",
                "current_projected_liability_usd"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-executive-compensation-rsu-tax-bracket-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(ExecutiveCompensationRSUTaxOptimizer, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-personal-agent-executive-compensation-rsu-tax-bracket-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-personal-agent-executive-compensation-rsu-tax-bracket-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
