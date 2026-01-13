import os
import subprocess

INVENTORY_FILE = "inventory/hosts.ini"
PLAYBOOK = "playbooks/site.yml"


def add_vm_to_inventory(vm_ips, group="new_vms"):
    """
    Add VM IPs to Ansible inventory dynamically
    """
    if not os.path.exists(INVENTORY_FILE):
        raise FileNotFoundError("Inventory file not found")

    with open(INVENTORY_FILE, "r") as f:
        content = f.read()

    if f"[{group}]" not in content:
        content += f"\n[{group}]\n"

    for ip in vm_ips:
        if ip not in content:
            content += f"{ip}\n"

    with open(INVENTORY_FILE, "w") as f:
        f.write(content)

    print(f"Added {len(vm_ips)} VM(s) to inventory group [{group}]")


def run_playbook():
    cmd = ["ansible-playbook", PLAYBOOK]
    try:
        subprocess.run(cmd, check=True)
        print("VM build and post checks completed successfully")
    except subprocess.CalledProcessError:
        print("Automation failed")


if __name__ == "__main__":
    # Example: Take VM IPs dynamically (can be from user / API / output)
    vm_ip_input = input("Enter VM IPs (comma separated): ")
    vm_ips = [ip.strip() for ip in vm_ip_input.split(",")]

    add_vm_to_inventory(vm_ips)
    run_playbook()
