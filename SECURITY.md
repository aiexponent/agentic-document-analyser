# Security Policy

AiExponent takes the security and integrity of our open-source AI governance software seriously. We appreciate the efforts of security researchers and practitioners who help us maintain high security standards.

## Supported Versions

We provide security updates and patches for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in **Agentic Document Analyser** or any affiliated service, please report it privately through coordinated vulnerability disclosure:

* **Email**: [security@aiexponent.com](mailto:security@aiexponent.com)
* **Encryption**: If desired, request our PGP public key via the security contact above prior to submission.
* **Public Issues**: **Do NOT open public GitHub issues, discussions, or pull requests for security vulnerabilities.** Public disclosure before a patch is released puts regulated deployments and users at risk.

### What to Include

To help us triage and remediate the issue efficiently, please include:
1. Type of vulnerability (e.g., SSRF, arbitrary code execution, denial of service, secret exposure).
2. Affected service(s) (`orchestrator`, `preprocessing_service`, `visual_service`, `frontend`, or shared libraries).
3. Step-by-step instructions or minimal proof-of-concept (PoC) to reproduce the vulnerability.
4. Any potential mitigations you have identified.

## Response Commitment & SLAs

We adhere to strict response timelines:

* **Initial Response**: Within **48 hours** of receiving your report, an engineer will acknowledge receipt and establish a secure communication channel.
* **Triage & Assessment**: Within **5 business days**, we will confirm the vulnerability, determine its severity (CVSS), and provide an estimated timeline for remediation.
* **Fix & Release**: Critical vulnerabilities are prioritized for hotfix releases, accompanied by a coordinated security advisory.

## Safe Harbor

AiExponent supports responsible, good-faith security research. If you make a good-faith effort to avoid privacy violations, data destruction, and service degradation during your research:
* We will not initiate legal action against you.
* We will work with you to understand and resolve the issue quickly.
* We will publicly credit your contribution in the security advisory (unless you prefer to remain anonymous).
