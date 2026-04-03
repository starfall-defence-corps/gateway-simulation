# Gateway Simulation — Troubleshooting Only

**This is an assessment.** No progressive hints. No spoilers. You have completed Module 1 — you know what to do.

This file exists only for common technical errors.

---

## SSH Connectivity

**"Permission denied (publickey)"**: Check that `.ssh/cadet_key` exists and has permissions 600. Re-run `make setup` if needed.

**"Connection refused"**: The containers may not be running. Check `docker ps`. Re-run `make setup`.

**"Host key verification failed"**: Your ansible.cfg should have `host_key_checking = False`. Check that it's set.

---

## Vault Issues

**"Decryption failed"**: Your `.vault-pass` content doesn't match the password used to encrypt `vault.yml`. The password should be `first-contact`.

**"vault_password_file" error**: If you haven't created `.vault-pass` yet, keep that line commented out in `ansible.cfg`. Uncomment it only after creating the file.

---

## Role Not Found

**"the role 'fleet_hardening' was not found"**: The role must be at `workspace/roles/fleet_hardening/`. Check `roles_path = roles` in `ansible.cfg`. Run Ansible from the `workspace/` directory.

---

## Firewall Issues

**ufw "ERROR: problem running"**: Run the playbook with `become: true`. The ufw module needs root.

**firewalld "not running"**: On Rocky Linux, firewalld may need to be started before rules can be added. Start the service first.

---

## Mixed OS

**Module not found**: Ensure Ansible collections are installed. `make setup` handles this, but if needed: `ansible-galaxy collection install community.general ansible.posix`

**"Conditional check failed"**: Check your `when` conditions. Use `ansible_os_family == "Debian"` (capital D) and `ansible_os_family == "RedHat"` (capital R, capital H).

---

*If none of the above helps, re-read the BRIEFING.md mission instructions. The answer is in your Module 1 training.*

*SDC Cyber Command — 2187*
