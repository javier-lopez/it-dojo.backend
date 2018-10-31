resource "digitalocean_ssh_key" "ssh-key" {
  public_key = "${file(var.public_key)}"
}
