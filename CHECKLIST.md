# Gateway Simulation: Operation First Contact — Progress Tracker

**Assessment**: Gateway Simulation (75 minutes)
**Rank Earned**: Ensign

**Start Time**: _______________
**End Time**: _______________

---

## Mission 1: Reconnaissance (20 min)

- [ ] Forward observation post is online (`make setup` succeeded)
- [ ] Inventory written at `inventory/hosts.yml`
- [ ] `debian` and `redhat` groups defined
- [ ] `group_vars/debian.yml` and `group_vars/redhat.yml` created
- [ ] `ansible all -m ping` succeeds on all 3 nodes
- [ ] Reconnaissance completed — ad-hoc commands used to assess state
- [ ] `RECON.md` filled in with findings

---

## Mission 2: Hardening (30 min)

- [ ] Role created: `ansible-galaxy init roles/fleet_hardening`
- [ ] `defaults/main.yml` has SSH and service variables
- [ ] `tasks/main.yml` has hardening tasks (SSH, firewall, services, sysctl, MOTD)
- [ ] `handlers/main.yml` has SSH restart handler
- [ ] `templates/sshd_config.j2` and `motd.j2` created
- [ ] `site.yml` uncommented and references role
- [ ] Syntax check passed
- [ ] First run: all nodes hardened
- [ ] Second run: `changed=0` (idempotent)

---

## Mission 3: Secure & Submit (25 min)

- [ ] `.vault-pass` created with password `first-contact`
- [ ] `vault.yml` created with sensitive values
- [ ] `vault.yml` encrypted (`$ANSIBLE_VAULT;` header)
- [ ] `ansible.cfg` updated with `vault_password_file`
- [ ] `site.yml` includes `vars_files: [vault.yml]`
- [ ] No plaintext secrets in workspace
- [ ] Final deployment successful
- [ ] `make test` — all 3 missions pass

---

## Performance Tier

| Time | Rating |
|------|--------|
| Under 45 min | Ace Cadet |
| 45–55 min | Distinguished |
| 55–65 min | Qualified |
| 65–75 min | Passed |
| 75+ min | RTB — retry |

**My Rating**: _______________
