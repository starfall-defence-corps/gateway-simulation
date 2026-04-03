"""
=== STARFALL DEFENCE CORPS ACADEMY ===
ARIA Automated Verification — Gateway Simulation: Operation First Contact
=========================================================================
"""
import os
import re
import subprocess
import yaml
import pytest


def _root_dir():
    """Return the mission root directory."""
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(tests_dir, "..", "..", ".."))


def _workspace_dir():
    return os.path.join(_root_dir(), "workspace")


def _role_dir():
    return os.path.join(_workspace_dir(), "roles", "fleet_hardening")


def _run_ansible(*args, **kwargs):
    """Run an ansible command from the workspace directory."""
    timeout = kwargs.pop("timeout", 90)
    result = subprocess.run(
        list(args),
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=_workspace_dir(),
    )
    return result


# -------------------------------------------------------------------
# Mission 1: Reconnaissance
# -------------------------------------------------------------------

class TestReconnaissance:
    """ARIA verifies: Has the cadet assessed the observation post?"""

    def test_inventory_exists(self):
        """Inventory file must exist at workspace/inventory/hosts.yml"""
        path = os.path.join(_workspace_dir(), "inventory", "hosts.yml")
        assert os.path.isfile(path), (
            "ARIA: No inventory found at inventory/hosts.yml. "
            "Write your fleet inventory — you know the nodes."
        )

    def test_inventory_has_groups(self):
        """Inventory must define debian and redhat groups"""
        path = os.path.join(_workspace_dir(), "inventory", "hosts.yml")
        if not os.path.isfile(path):
            pytest.skip("Inventory does not exist yet")
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None, (
            "ARIA: Inventory file is empty."
        )
        # Flatten all keys recursively to find group names
        all_keys = set()
        _collect_keys(data, all_keys)
        has_debian = any(k in all_keys for k in ("debian", "Debian"))
        has_redhat = any(k in all_keys for k in ("redhat", "RedHat", "redhat_servers"))
        assert has_debian and has_redhat, (
            "ARIA: Inventory must define 'debian' and 'redhat' groups. "
            "The fleet runs mixed OS — your inventory must reflect that."
        )

    def test_group_vars_exist(self):
        """group_vars files must exist for OS-specific settings"""
        gv_dir = os.path.join(_workspace_dir(), "inventory", "group_vars")
        if not os.path.isdir(gv_dir):
            # Also check workspace/group_vars (alternate location)
            gv_dir = os.path.join(_workspace_dir(), "group_vars")
        assert os.path.isdir(gv_dir), (
            "ARIA: No group_vars directory found. Create "
            "inventory/group_vars/ with OS-specific variables."
        )
        files = os.listdir(gv_dir)
        yml_files = [f for f in files if f.endswith((".yml", ".yaml"))]
        assert len(yml_files) >= 2, (
            "ARIA: group_vars needs at least 2 files (one per OS family). "
            "Define variables for debian.yml and redhat.yml."
        )

    def test_recon_md_completed(self):
        """RECON.md must have findings documented (not just template)"""
        path = os.path.join(_workspace_dir(), "RECON.md")
        assert os.path.isfile(path), (
            "ARIA: RECON.md not found in workspace/."
        )
        with open(path) as f:
            content = f.read()
        # Check that at least some template sections have been filled in
        # Count non-empty lines that aren't headers or template markers
        filled_lines = []
        for line in content.splitlines():
            stripped = line.strip()
            if (stripped
                    and not stripped.startswith("#")
                    and not stripped.startswith("|")
                    and not stripped.startswith("---")
                    and not stripped.startswith("<!--")
                    and not stripped.startswith("*")
                    and not stripped.startswith("**")
                    and stripped not in ("", "_______________")):
                filled_lines.append(stripped)
        assert len(filled_lines) >= 5, (
            "ARIA: RECON.md appears mostly empty. Document your "
            "reconnaissance findings — services, vulnerabilities, plan."
        )


# -------------------------------------------------------------------
# Mission 2: Hardening
# -------------------------------------------------------------------

class TestHardening:
    """ARIA verifies: Has the cadet secured the observation post?"""

    def test_role_directory_exists(self):
        """Role must exist at roles/fleet_hardening/"""
        assert os.path.isdir(_role_dir()), (
            "ARIA: No role found at roles/fleet_hardening/. "
            "Create it with: ansible-galaxy init roles/fleet_hardening"
        )

    def test_tasks_main_has_content(self):
        """tasks/main.yml must have hardening tasks"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        path = os.path.join(_role_dir(), "tasks", "main.yml")
        assert os.path.isfile(path), (
            "ARIA: tasks/main.yml not found in role."
        )
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None and isinstance(data, list) and len(data) >= 3, (
            "ARIA: tasks/main.yml needs at least 3 tasks. You should "
            "have SSH, firewall, and template tasks at minimum."
        )

    def test_handlers_exist(self):
        """handlers/main.yml must have at least one handler"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        path = os.path.join(_role_dir(), "handlers", "main.yml")
        assert os.path.isfile(path), (
            "ARIA: handlers/main.yml not found."
        )
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None and isinstance(data, list) and len(data) >= 1, (
            "ARIA: handlers/main.yml is empty. Add your SSH restart handler."
        )

    def test_templates_exist(self):
        """templates/ must have at least one .j2 file"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        path = os.path.join(_role_dir(), "templates")
        assert os.path.isdir(path), (
            "ARIA: templates/ directory not found in role."
        )
        templates = [f for f in os.listdir(path) if f.endswith(".j2")]
        assert len(templates) >= 1, (
            "ARIA: No .j2 templates found. Create sshd_config.j2 at minimum."
        )

    def test_defaults_have_variables(self):
        """defaults/main.yml must have variable definitions"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        defaults = os.path.join(_role_dir(), "defaults", "main.yml")
        role_vars = os.path.join(_role_dir(), "vars", "main.yml")
        has_content = False
        for p in (defaults, role_vars):
            if os.path.isfile(p):
                with open(p) as f:
                    data = yaml.safe_load(f)
                if data and isinstance(data, dict) and len(data) >= 1:
                    has_content = True
                    break
        assert has_content, (
            "ARIA: No variable definitions found in defaults/ or vars/. "
            "Define SSH settings, service names, and other parameters."
        )

    def test_ssh_hardened_all_nodes(self):
        """SSH root login must be disabled on all nodes"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        result = _run_ansible(
            "ansible", "all", "-m", "shell",
            "-a", "grep -E '^PermitRootLogin\\s+no' /etc/ssh/sshd_config",
        )
        assert result.returncode == 0, (
            "ARIA: SSH is not hardened on all nodes. "
            "Run your playbook: ansible-playbook site.yml"
        )

    def test_firewall_active(self):
        """Firewall must be active on all nodes"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        # Check Debian nodes (ufw)
        result_deb = _run_ansible(
            "ansible", "debian", "-m", "shell",
            "-a", "ufw status | grep -q 'Status: active'",
        )
        # Check RedHat nodes (firewalld)
        result_rh = _run_ansible(
            "ansible", "redhat", "-m", "shell",
            "-a", "firewall-cmd --state 2>/dev/null | grep -q running",
        )
        assert result_deb.returncode == 0 and result_rh.returncode == 0, (
            "ARIA: Firewall is not active on all nodes. "
            "Ensure ufw (Debian) and firewalld (RedHat) are running."
        )

    def test_telnet_removed(self):
        """Telnet must be removed from Debian nodes"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        result = _run_ansible(
            "ansible", "debian", "-m", "shell",
            "-a", "dpkg -l telnet 2>/dev/null | grep -q '^ii' && echo FOUND || echo GONE",
        )
        assert "FOUND" not in result.stdout, (
            "ARIA: Telnet is still installed on Debian nodes. "
            "Remove it — insecure services have no place on fleet systems."
        )

    def test_motd_deployed(self):
        """Login banner must be deployed on all nodes"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        result = _run_ansible(
            "ansible", "all", "-m", "shell",
            "-a", "cat /etc/motd",
        )
        assert result.returncode == 0 and "STARFALL" in result.stdout, (
            "ARIA: Login banner not deployed. Deploy an MOTD template "
            "that identifies the node."
        )

    def test_sysctl_hardened(self):
        """Kernel hardening must be applied"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        result = _run_ansible(
            "ansible", "debian", "-m", "shell",
            "-a", "sysctl net.ipv4.ip_forward",
        )
        if result.returncode != 0:
            pytest.skip("Cannot check sysctl — fleet not yet hardened")
        assert "= 0" in result.stdout, (
            "ARIA: IP forwarding still enabled. Deploy hardened sysctl configuration."
        )

    def test_idempotent(self):
        """Running site.yml must show changed=0"""
        if not os.path.isdir(_role_dir()):
            pytest.skip("Role does not exist yet")
        # Check if hardening has been applied
        check = _run_ansible(
            "ansible", "all", "-m", "shell",
            "-a", "grep -E '^PermitRootLogin\\s+no' /etc/ssh/sshd_config",
        )
        if check.returncode != 0:
            pytest.skip("Fleet not yet hardened — run site.yml first")
        result = _run_ansible(
            "ansible-playbook", "site.yml",
            timeout=120,
        )
        assert result.returncode == 0, (
            "ARIA: site.yml failed on second run. Fix errors."
        )
        changed_match = re.findall(r"changed=(\d+)", result.stdout)
        total_changed = sum(int(c) for c in changed_match)
        assert total_changed == 0, (
            f"ARIA: Idempotency failure — {total_changed} task(s) changed "
            f"on second run. A good role produces the same result every time."
        )


# -------------------------------------------------------------------
# Mission 3: Secure & Submit
# -------------------------------------------------------------------

class TestSecureAndSubmit:
    """ARIA verifies: Are secrets secured and playbook properly structured?"""

    def test_vault_file_exists(self):
        """vault.yml must exist in workspace/"""
        path = os.path.join(_workspace_dir(), "vault.yml")
        assert os.path.isfile(path), (
            "ARIA: vault.yml not found. Create it with: "
            "ansible-vault create vault.yml"
        )

    def test_vault_file_encrypted(self):
        """vault.yml must be encrypted"""
        path = os.path.join(_workspace_dir(), "vault.yml")
        if not os.path.isfile(path):
            pytest.skip("vault.yml does not exist yet")
        with open(path) as f:
            first_line = f.readline().strip()
        assert first_line.startswith("$ANSIBLE_VAULT;"), (
            "ARIA: vault.yml is NOT encrypted. Encrypt it: "
            "ansible-vault encrypt vault.yml"
        )

    def test_vault_pass_exists(self):
        """.vault-pass must exist for automated decryption"""
        path = os.path.join(_workspace_dir(), ".vault-pass")
        assert os.path.isfile(path), (
            "ARIA: .vault-pass not found. Create it with your vault "
            "password. This file is gitignored."
        )

    def test_no_plaintext_secrets(self):
        """No plaintext passwords or API keys in workspace"""
        sensitive_patterns = [
            "V01dborn_Hunter_2187",
            "sk-sdc-1a2b3c4d5e6f7g8h9i0j",
            "fleet_db_pass",
            "fleet_api_key",
        ]
        violations = []
        for root, dirs, files in os.walk(_workspace_dir()):
            dirs[:] = [d for d in dirs if d not in (".ssh", "__pycache__", ".git")]
            for fname in files:
                fpath = os.path.join(root, fname)
                if fname.endswith((".pyc", ".key")):
                    continue
                # RECON.md documents findings — it's not storing secrets
                if fname == "RECON.md":
                    continue
                try:
                    with open(fpath) as f:
                        content = f.read()
                except (UnicodeDecodeError, PermissionError):
                    continue
                if content.startswith("$ANSIBLE_VAULT;"):
                    continue
                for pattern in sensitive_patterns:
                    if pattern in content:
                        rel = os.path.relpath(fpath, _workspace_dir())
                        violations.append(f"{rel} contains '{pattern}'")
        assert not violations, (
            "ARIA: Plaintext secrets detected!\n"
            + "\n".join(f"  - {v}" for v in violations)
            + "\nEncrypt sensitive values in vault.yml."
        )

    def test_site_yml_references_role(self):
        """site.yml must reference fleet_hardening role and vault.yml"""
        path = os.path.join(_workspace_dir(), "site.yml")
        assert os.path.isfile(path), (
            "ARIA: site.yml not found."
        )
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data is not None and isinstance(data, list), (
            "ARIA: site.yml is empty or invalid YAML."
        )
        play = data[0]
        # Check role reference
        roles = play.get("roles") or []
        role_names = []
        for r in roles:
            if isinstance(r, str):
                role_names.append(r)
            elif isinstance(r, dict):
                role_names.append(r.get("role", r.get("name", "")))
        assert "fleet_hardening" in role_names, (
            "ARIA: site.yml does not reference the fleet_hardening role."
        )
        # Check vars_files reference
        vars_files = play.get("vars_files") or []
        has_vault = any("vault" in str(v) for v in vars_files)
        assert has_vault, (
            "ARIA: site.yml does not include vault.yml in vars_files. "
            "Add: vars_files: [vault.yml]"
        )


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def _collect_keys(obj, keys_set):
    """Recursively collect all dictionary keys."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys_set.add(k)
            _collect_keys(v, keys_set)
    elif isinstance(obj, list):
        for item in obj:
            _collect_keys(item, keys_set)
