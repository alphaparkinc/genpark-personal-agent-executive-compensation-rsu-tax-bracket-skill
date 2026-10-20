# Executive Compensation RSU & Equity Tax Bracket Copilot Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Tech employee executive equity audit, RSU vest date withholding deficit estimation, AMT ISO exercise modeling, and dynamic 83(b) election arbiter. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `audit_rsu_vesting_tax_deficit`: Audit upcoming RSU vests for statutory 22% supplemental withholding shortfall against actual 37% marginal federal tax bracket.
- `synthesize_quarterly_estimated_tax_plan`: Synthesize IRS Form 1040-ES quarterly estimated tax voucher allocations to eliminate underpayment penalty (IRC 6654).

## 🚀 Installation & Usage
Run directly with pure Python standard library:
```bash
python -m genpark_personal_agent_executive_compensation_rsu_tax_bracket_skill.server --test
```
