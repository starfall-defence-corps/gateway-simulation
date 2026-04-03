---
CLASSIFICATION: CADET EYES ONLY
ASSESSMENT: GATEWAY SIMULATION — OPERATION FIRST CONTACT
THEATRE: Starfall Defence Corps Academy
AUTHORITY: SDC Cyber Command, 2187
---

# GATEWAY SIMULATION — OPERATION: FIRST CONTACT

---

## 1. SITUATION

### 1a. Enemy Forces

The Voidborn have compromised a **forward observation post**. Three nodes exposed. SSH wide open. Firewalls down. Insecure services running. Hardcoded credentials on the filesystem. Kernel hardening absent. No login banners. The post is a liability.

This is everything you have trained to fix.

### 1b. Friendly Forces

Over five missions, you have learned:
- Inventory and ad-hoc commands (1.1)
- Playbook fundamentals and SSH hardening (1.2)
- Service management, packages, and firewall (1.3)
- Variables, templates, and multi-OS support (1.4)
- Roles, Vault, and Git workflow (1.5)

Now prove you can do it all. Under pressure. From scratch.

### 1c. Attachments / Support

**ARIA** will verify your work across three missions. Run `make test` at any time.

**No hints file.** You have completed Module 1. You know what to do.

---

## 2. MISSION

Secure the forward observation post. Three missions, 75 minutes total.

| Mission | Time | Objective |
|---------|------|-----------|
| 1. Reconnaissance | 20 min | Assess the post, write inventory, document findings |
| 2. Hardening | 30 min | Build a role, harden everything, deploy |
| 3. Secure & Submit | 25 min | Vault secrets, clean structure, verify |

**End state**: All nodes hardened. SSH locked down. Firewalls active. Insecure services removed. Kernel hardened. Secrets encrypted. Role-based. Idempotent. ARIA approves.

---

## 3. EXECUTION

### 3a. Commander's Intent

This simulation tests whether you can combine every skill from Module 1 without step-by-step guidance. Speed matters, but correctness matters more. A fast deployment that leaves root login enabled is worse than a slow one that doesn't.

### 3b. Forward Observation Post — Fleet Assets

| Designation | OS | SSH Port | Network |
|-------------|----|----------|---------|
| `sdc-fwd-web` | Ubuntu 22.04 | 2231 | 172.31.0.11 |
| `sdc-fwd-db` | Rocky Linux 9 | 2232 | 172.31.0.12 |
| `sdc-fwd-comms` | Ubuntu 22.04 | 2233 | 172.31.0.13 |

**SSH user**: `cadet` (key-based auth, key at `.ssh/cadet_key`)

### 3c. Known Compromises

Intelligence reports the following on every node:
- SSH: root login enabled, password authentication enabled
- No login banner (MOTD)

Additionally, on Ubuntu nodes:
- `telnet` and `xinetd` installed (insecure services)
- Firewall (ufw) installed but **inactive**
- `/etc/shadow` permissions too open (0644, should be 0640)
- No kernel hardening (IP forwarding enabled, no SYN flood protection)

On the Rocky Linux node:
- Firewalld enabled but SSH not explicitly allowed
- Hardcoded credentials at `/opt/fleet-db-creds.txt`

**Note**: The credential file exists on ALL nodes. Check every one.

### 3d. Mission 1: Reconnaissance (20 minutes)

1. **Activate your environment**: `source venv/bin/activate`

2. **Write your inventory** at `inventory/hosts.yml`
   - Define `debian` and `redhat` parent groups
   - Assign nodes to correct groups
   - Include connection details (host, port, user, key)

3. **Create group_vars** at `inventory/group_vars/`
   - `debian.yml` — SSH service name, firewall package
   - `redhat.yml` — SSH service name, firewall package
   - `all.yml` — shared SSH settings (optional)

4. **Test connectivity**: `ansible all -m ping`

5. **Reconnaissance**: Use ad-hoc commands to assess the post
   - `ansible all -m shell -a "cat /etc/ssh/sshd_config | grep -i permit"`
   - `ansible debian -m shell -a "ufw status"`
   - `ansible all -m shell -a "cat /opt/fleet-db-creds.txt"`
   - `ansible debian -m shell -a "dpkg -l telnet"`
   - `ansible debian -m shell -a "sysctl net.ipv4.ip_forward"`
   - `ansible debian -m shell -a "stat -c '%a' /etc/shadow"`

6. **Document findings** in `RECON.md` — fill in every section

### 3e. Mission 2: Hardening (30 minutes)

1. **Create the role**: `ansible-galaxy init roles/fleet_hardening`

2. **Build the role** — at minimum:
   - `defaults/main.yml` — SSH settings, service names, firewall packages
   - `tasks/main.yml` — SSH config, MOTD, firewall, services, sysctl, permissions
   - `handlers/main.yml` — SSH restart handler
   - `templates/` — `sshd_config.j2`, `motd.j2`

3. **Write site.yml** — uncomment and complete (hosts, become, roles)

4. **Syntax check**: `ansible-playbook site.yml --syntax-check`

5. **Deploy**: `ansible-playbook site.yml`

6. **Verify idempotency**: Run again — `changed=0` on all hosts

### 3f. Mission 3: Secure & Submit (25 minutes)

1. **Create vault password file**:
   ```bash
   echo 'first-contact' > .vault-pass
   chmod 600 .vault-pass
   ```

2. **Uncomment** `vault_password_file = .vault-pass` in `ansible.cfg`

3. **Create and encrypt vault.yml**:
   ```bash
   # Create with your sensitive values
   cat > vault.yml << 'EOF'
   vault_ssh_login_grace_time: 30
   vault_banner_message: "STARFALL DEFENCE CORPS — FORWARD OBSERVATION POST"
   EOF
   ansible-vault encrypt vault.yml
   ```

4. **Update site.yml** to include `vars_files: [vault.yml]`

5. **Update role defaults** to reference vault variables where appropriate

6. **Run final deployment**: `ansible-playbook site.yml`

7. **Verify**: `make test` — all three missions must pass

### 3g. Rules of Engagement

- No looking at other missions' solution files during the assessment
- You may consult official Ansible documentation
- The `files/sysctl-hardened.conf` is provided — use it
- Vault password must be `first-contact` (ARIA needs to verify vault contents)

---

## 4. PERFORMANCE TIERS

| Time | Rating |
|------|--------|
| Under 45 min | **Ace Cadet** |
| 45–55 min | **Distinguished** |
| 55–65 min | **Qualified** |
| 65–75 min | **Passed** |
| 75+ min | **RTB** (Return to Base — retry) |

Record your start time. Record your end time. Be honest.

---

## 5. COMMAND AND SIGNAL

**Commander's Final Order**: This is the test. Everything you have learned. Every module, every skill, under the clock. The forward observation post depends on you. Secure it. Document it. Encrypt it. Deploy it.

When ARIA confirms all three missions, you have earned the rank of **Ensign**.

The Starfall Defence Corps salutes your service, Cadet. Now prove you're ready.

**Start your timer. Begin.**

---

*SDC Cyber Command — 2187 — CADET EYES ONLY*
