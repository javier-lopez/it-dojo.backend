resource "digitalocean_droplet" "app" {
    count    = "1"
    name     = "app-${count.index}"
    region   = "sfo2"
    image    = "ubuntu-16-04-x64"
    size     = "512mb"
    ssh_keys = [ "${var.ssh_fingerprint}" ]
    private_networking = true

    connection {
        user = "root"
        type = "ssh"
        private_key = "${file(var.pvt_key)}"
        timeout = "2m"
    }

    provisioner "remote-exec" {
        inline = [
            #echo executed cmds
            "set -x",
            #install ansible deps
            "apt-get -y update && apt-get -y install python python-pip sudo",
            #enable passwordless sudo wheel group
            "addgroup wheel",
            "echo '%wheel ALL = (ALL) NOPASSWD: ALL' | tee /etc/sudoers.d/wheel",
            #create ansible user
            "adduser --quiet --disabled-password --shell /bin/bash --home /home/ansible --gecos 'User' ansible",
            "echo 'ansible:ansible' | chpasswd",
            "usermod -a -G wheel ansible",
            #enable ssh access
            "mkdir /home/ansible/.ssh",
            "cp -r ~/.ssh/authorized_keys /home/ansible/.ssh/authorized_keys",
            "chown -R ansible:ansible /home/ansible/.ssh"
        ]
    }
}
