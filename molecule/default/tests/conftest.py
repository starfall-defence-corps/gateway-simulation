"""
ARIA Custom Test Reporter
Provides color-coded, phase-grouped output for Gateway Simulation verification.

Writes all output to stderr so check-work.sh can discard pytest's
default stdout while preserving our formatted display.
"""
import os
import pytest
import sys

# -- Phase and test name mappings -------------------------------------------

PHASES = {
    "TestReconnaissance":   ("1", "Reconnaissance"),
    "TestHardening":        ("2", "Hardening"),
    "TestSecureAndSubmit":  ("3", "Secure & Submit"),
}

FRIENDLY = {
    "test_inventory_exists":             "Inventory file exists",
    "test_inventory_has_groups":         "Inventory has debian/redhat groups",
    "test_group_vars_exist":             "group_vars files exist",
    "test_recon_md_completed":           "RECON.md has findings documented",
    "test_role_directory_exists":        "Role directory exists",
    "test_tasks_main_has_content":       "tasks/main.yml has tasks",
    "test_handlers_exist":               "handlers/main.yml has handlers",
    "test_templates_exist":              "templates/ has .j2 files",
    "test_defaults_have_variables":      "defaults/ has variable definitions",
    "test_ssh_hardened_all_nodes":       "SSH hardened on all nodes",
    "test_firewall_active":              "Firewall active on all nodes",
    "test_telnet_removed":               "Telnet removed from Debian nodes",
    "test_motd_deployed":                "Login banner deployed",
    "test_sysctl_hardened":              "Kernel hardening applied",
    "test_idempotent":                   "Role is idempotent (changed=0)",
    "test_vault_file_exists":            "vault.yml exists",
    "test_vault_file_encrypted":         "vault.yml is encrypted",
    "test_vault_pass_exists":            ".vault-pass file exists",
    "test_no_plaintext_secrets":         "No plaintext secrets in workspace",
    "test_site_yml_references_role":     "site.yml references role + vault",
}

# -- Reporter ---------------------------------------------------------------

# The phase-oriented summary is rendered by the shared `aria-reporter`
# pytest plugin (installed via requirements.txt); this file only declares
# the mission's phases + friendly objective names.
from aria_reporter import configure  # noqa: E402

configure(
    phases=PHASES, friendly=FRIENDLY,
    mission_id="gateway", unit="Mission",
)
