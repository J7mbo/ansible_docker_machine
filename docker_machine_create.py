#!/usr/bin/python

# Copyright: (c) 2020, James Mallison <jm_cj<at>hotmail<dot>com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
import shlex
import subprocess

from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: docker_machine_create

short_description: Executes docker-machine create --driver generic with the given ip address and ssh key

version_added: "2.7"

description:
    - "Require the ability to install docker on some node you've provisioned with, say, terraform? You can do this with
       docker machine create which handles it all for oyu. You could use shell in ansible, or you could use this, 
       which does it for you. Nothing complex."

options:
    name:
        description:
            - The name of the machine to create
        required: true    
    ip:
        description:
            - This is for --generic-ip-address
        required: true
    ssh_key:
        description:
            - This is for --generic-ssh-key
        required: true

author:
    - James Mallison (@j7mbo)
'''

EXAMPLES = '''
# Create a docker-machine with generic driver, ip and ssh key
- name: "Create docker-machine"
  docker_machine_create:
    ip: {{ machine_ip }}
    ssh_key: {{ machine_ssh_key }}
'''

RETURN = '''
message:
    description: The output message that the module generates
    type: str
    returned: always
'''


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        ip=dict(type='str', required=False, default=False),
        ssh_key=dict(type='str', required=False, default=False)
    )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # In check mode, only show the current state.
    if module.check_mode:
        proc = subprocess.Popen(shlex.split("docker-machine ls"), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = proc.communicate()

        result.message = out
        module.exit_json(**result)

    cmd = 'docker-machine create --driver generic --generic-ip-address {ip} --generic-ssh-key {ssh_key} {name}'

    proc = subprocess.Popen(
        shlex.split(
            cmd.format(
                ip=module.params['ip'],
                ssh_key=module.params['ssh_key'],
                name=module.params['name']
            )
        ),
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

    out, err = proc.communicate()

    result['message'] = out

    if 'already exists' in err:
        module.exit_json(**result)

    if 'command not found' in err:
        module.fail_json(msg='docker-machine not found - are you sure it is installed and in the path?', **result)

    if 'Docker is up and running' not in out:
        module.fail_json(msg='unknown response from docker-machine', **result)

    result['changed'] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
