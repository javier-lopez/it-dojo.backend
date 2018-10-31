resource "digitalocean_droplet" "docker-manager" {
    count    = "1"
    name     = "${format("docker-manager-%02d", count.index)}"
    region   = "sfo2"
    image    = "ubuntu-16-04-x64"
    size     = "s-1vcpu-1gb"
    private_networking = true

    ssh_keys = ["${digitalocean_ssh_key.ssh-key.id}"]

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

output "docker-manager-output" {
  value = "${digitalocean_droplet.docker-manager.*.ipv4_address}"
}

resource "digitalocean_floating_ip" "docker-manager-ip-flotante" {
  droplet_id = "${digitalocean_droplet.docker-manager.0.id}"
  region     = "${digitalocean_droplet.docker-manager.0.region}"
}

output "docker-manager-ip-flotante-output" {
  value = "${digitalocean_floating_ip.docker-manager-ip-flotante.*.ip_address}"
}

#cost too much, $20 per month, using floating ips instead
#resource "digitalocean_loadbalancer" "load-balancer" {
  #name   = "load-balancer"
  #region = "sfo2"

  #forwarding_rule {
    #entry_port      = 80
    #entry_protocol  = "http"

    #target_port     = 80
    #target_protocol = "http"
  #}

  #healthcheck {
    #port     = 80
    #protocol = "http"
  #}

  #droplet_ids = ["${digitalocean_droplet.docker-manager.*.id}"]
#}

#output "load-balancer-ip" {
  #value = "${digitalocean_loadbalancer.load-balancer.*.ip}"
#}
