
data "scaleway_account_ssh_key" "main" {
  ssh_key_id = var.ssh_key_id
}

resource "scaleway_instance_ip" "server_ip" {}

resource "scaleway_instance_server" "devbox" {

  depends_on = [data.scaleway_account_ssh_key.main]

  name  = var.names["Name"]
  type  = var.instance_type
  image = var.instance_image
  zone  = var.zone

  tags = [
    var.names["Name"],
    var.environment,
    "devbox"
  ]

  ip_id = scaleway_instance_ip.server_ip.id
  enable_ipv6 = true

  security_group_id = var.security_group_id

  additional_volume_ids = var.volume_id == null ? null : [var.volume_id]

}