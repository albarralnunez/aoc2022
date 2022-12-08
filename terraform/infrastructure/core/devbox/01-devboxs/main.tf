provider "scaleway" {
  zone       = var.zone
  region     = var.region
  project_id = var.project_id
}

module "danielalbarral-devbox-names" {
  source            = "../../../../modules/naming"
  region            = var.region
  environment       = var.environment
  project_name      = var.project_name
  project_component = "danielalbarral-devbox"
}

module "devbox-sg-names" {
  source            = "../../../../modules/naming"
  region            = var.region
  environment       = var.environment
  project_name      = var.project_name
  project_component = "devbox-sg"
}

resource "scaleway_instance_security_group" "devbox-sg" {
  name                    = module.devbox-sg-names.naming["Name"]
  inbound_default_policy  = "drop"
  outbound_default_policy = "accept"

  inbound_rule {
    action   = "accept"
    port     = 22
    ip_range = "::/0"
  }

  inbound_rule {
    action   = "accept"
    port     = 22
    ip_range = "0.0.0.0/0"
  }

}


module "danielalbarral-devbox" {
  source            = "../../../../modules/scaleway/devbox"
  names             = module.danielalbarral-devbox-names.naming
  environment       = var.environment
  zone              = var.zone
  instance_image    = var.instance_image
  ssh_key_id        = var.danielalbarral_ssh_key_id
  instance_type     = var.instance_type
  security_group_id = scaleway_instance_security_group.devbox-sg.id
}
