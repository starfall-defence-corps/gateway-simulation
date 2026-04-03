# Starfall Defence Corps Academy

## Gateway Simulation: Operation First Contact

> *"The Voidborn have compromised a forward observation post. Three nodes exposed. 75 minutes. Everything you've learned."*

This is the **Gateway Simulation** — the capstone assessment for Module 1 (Basic Training). You must combine every skill from Missions 1.1–1.5 to secure a compromised observation post under time pressure. No step-by-step guide. No hints. Just a briefing and a timer.

**Pass this simulation and earn the rank of Ensign.**

## Prerequisites

- Completed Missions 1.1 through 1.5
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Docker Compose v2)
- [GNU Make](https://www.gnu.org/software/make/)
- Python 3.10+ (for test environment)
  - On Debian/Ubuntu: `sudo apt install python3-venv`
- Git

> **Windows users**: Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and run all commands from within your WSL terminal.

## Quick Start

```bash
# 1. Use this template on GitHub (green button, top right)
git clone https://github.com/YOUR-USERNAME/gateway-simulation.git
cd gateway-simulation

# 2. Launch the forward observation post
make setup

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Start your timer. Read the briefing.
```

Read your orders: [Mission Briefing](docs/BRIEFING.md)

## Lab Architecture

```
 Your Machine
+----------------------------------------------------+
|  workspace/                                        |
|    ansible.cfg           (pre-configured)          |
|    RECON.md              (you fill in)             |
|    site.yml              (you write)               |
|    vault.yml             (you create + encrypt)    |
|    .vault-pass           (you create, gitignored)  |
|    inventory/            (you write from scratch)  |
|    roles/                                          |
|      fleet_hardening/    (you create via galaxy)   |
|    files/                                          |
|      sysctl-hardened.conf (provided)               |
|                                                    |
|  Docker Network: 172.31.0.0/24                     |
|  +--------------+ +---------------+ +-----------+  |
|  | sdc-fwd-web  | | sdc-fwd-db    | | sdc-fwd-  |  |
|  | :2231        | | :2232         | | comms     |  |
|  | Ubuntu 22.04 | | Rocky Linux 9 | | :2233     |  |
|  |              | |               | | Ubuntu    |  |
|  | Compromised — SSH open, firewall down,        |  |
|  | telnet running, creds on disk, no hardening   |  |
|  +--------------+ +---------------+ +-----------+  |
+----------------------------------------------------+
```

## Available Commands

```
make help       Show available commands
make setup      Launch the forward observation post (3 nodes)
make test       Ask ARIA to verify your work
make reset      Destroy and rebuild all nodes
make destroy    Tear down everything (containers, keys, venv)
make ssh-web    SSH into sdc-fwd-web (Ubuntu)
make ssh-db     SSH into sdc-fwd-db (Rocky Linux)
make ssh-comms  SSH into sdc-fwd-comms (Ubuntu)
```

## Assessment Structure

| Mission | Time | What ARIA Checks |
|---------|------|-----------------|
| 1. Reconnaissance | 20 min | Inventory, group_vars, RECON.md |
| 2. Hardening | 30 min | Role structure, SSH, firewall, MOTD, sysctl, idempotency |
| 3. Secure & Submit | 25 min | Vault encryption, no plaintext secrets, site.yml structure |

## Performance Tiers

| Time | Rating |
|------|--------|
| Under 45 min | Ace Cadet |
| 45–55 min | Distinguished |
| 55–65 min | Qualified |
| 65–75 min | Passed |
| 75+ min | RTB (Return to Base) |

## ARIA Review (Pull Request Workflow)

**Locally** — run `make test` for instant verification.

**On Pull Request** — push your work, open a PR, ARIA reviews automatically.

To enable PR reviews, add `ANTHROPIC_API_KEY` to your repo's Secrets (Settings > Secrets > Actions).

## Troubleshooting

**SSH issues**: Run `make setup` first. Check `docker ps` to verify containers are running.

**Vault errors**: The vault password is `first-contact`. Ensure `.vault-pass` contains exactly that.

**Need a clean slate**: Run `make reset` to rebuild containers. Your workspace files are preserved.
