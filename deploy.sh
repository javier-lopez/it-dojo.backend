#!/bin/sh
CURRENT_DIR="$(cd "$(dirname "${0}")" && pwd)"

set -x

cd "${CURRENT_DIR}"
cd provision/ansible/

if [ ! -f ../../.vault_pass.txt ]; then
    printf "%s\\n" "$(realpath ../../.vault_pass.txt) doesn't exists, exiting ..."
    exit 1
fi

ansible-playbook docker-swarm.yml -i inventories/prod/hosts -u ansible --private-key=~/.ssh/id_rsa --vault-password-file ../../.vault_pass.txt
