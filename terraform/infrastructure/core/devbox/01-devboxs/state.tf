terraform {
  backend "s3" {
    bucket                      = "aoc2022-terraform-state"
    key                         = "terraform.infrastructure.core.devbox.01-devboxs.tfstate"
    region                      = "fr-par"
    endpoint                    = "https://s3.fr-par.scw.cloud"
    skip_credentials_validation = true
    skip_region_validation      = true
  }
}
