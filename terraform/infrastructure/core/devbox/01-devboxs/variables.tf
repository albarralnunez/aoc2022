variable "environment" {
  type        = string
  description = "Environment"
}

variable "project_id" {
  type        = string
  description = "Your project ID."
}

variable "project_name" {
  type        = string
  description = "Project name."
}

variable "region" {
  type        = string
  description = "Region"
  validation {
    condition     = contains(["nl-ams", "fr-par"], var.region)
    error_message = "Valid values for var: test_variable are (nl-ams, fr-par)."
  }
}

variable "zone" {
  type        = string
  description = "Zone"
  validation {
    condition     = contains(["nl-ams-1", "fr-par-1"], var.zone)
    error_message = "Valid values for var: test_variable are (nl-ams-1, fr-par-1)."
  }
}

variable "instance_image" {
  type        = string
  description = "value of the image to use"
  default     = "ubuntu_focal"
}

variable "instance_type" {
  type        = string
  description = "value of the instance type to use"
  default     = "PLAY2-PICO"
}

variable "danielalbarral_ssh_key_id" {
  type        = string
  description = "SSH key id."
}
