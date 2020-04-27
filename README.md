docker_machine_create
--

Overview
--

This is a very simple ansible module to run `docker-machine create` idempotently for you for infrastructure you have 
already provisioned.

Description
--

Require the ability to install docker on some node you've provisioned with, say, terraform? You can do this with docker-machine 
create which not only installs and configures docker for you but sets up an ssh configuration so you can run `docker-machine ssh`
to connect to those machines. 

Let's say you want to do this with ansible. You could use `shell` in ansible, or you could use this, which does it for you. Nothing complex.

The actual command executed looks like this:

```
docker-machine create --driver generic --generic-ip-address {ip} --generic-ssh-key {ssh_key} {name}
```

How to use
--

Here is the **task**, which goes in your playbook:

```
- name: "Create docker-machine"
  docker_machine_create:
    ip: {{ machine_ip }}
    ssh_key: {{ machine_ssh_key }}
```

To use this module locally, you can follow the instructions [here](https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html). 
Just create a directory called `library/` where your playbook is and check out this python file in it or just copy and paste it.

--dry-run
--

If you run ansible with `--dry-run`, it'll just print out the output from `docker-machine ls` for you without effecting any changes.
