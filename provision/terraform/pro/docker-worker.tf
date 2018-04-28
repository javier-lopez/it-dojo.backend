resource "digitalocean_droplet" "docker-worker" {
    count    = "2"
    name     = "${format("docker-worker-%02d", count.index)}"
    region   = "sfo2"
    image    = "ubuntu-16-04-x64"
    size     = "s-1vcpu-1gb"
    private_networking = true

    ssh_keys = ["${digitalocean_ssh_key.it-dojo-key.id}"]

    connection {
        user = "root"
        type = "ssh"
        private_key = "${file(var.private_key)}"
        timeout = "2m"
    }

    provisioner "remote-exec" {
        script = "provision/01-disable-unattended-upgrades.sh"
    }

    provisioner "remote-exec" {
        script = "provision/02-install-ansible-deps.sh"
    }
}

output "docker-worker-ip" {
  value = "${digitalocean_droplet.docker-worker.*.ipv4_address}"
}
