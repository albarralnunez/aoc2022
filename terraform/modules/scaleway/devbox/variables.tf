variable "names" {
  type        = map(string)
  description = "Name convention for the variables"
}

variable "environment" {
  type        = string
  description = "Environment."
}

variable "zone" {
  type        = string
  description = "Zone."
  validation {
    condition     = contains(["nl-ams-1", "fr-par-1"], var.zone)
    error_message = "Valid values for var: test_variable are (nl-ams-1, fr-par-1)."
  }
}

variable "volume_id" {
  type        = string
  description = "ID of the extra volume to attach to the instance."
  default     = null
}

variable "instance_image" {
  type        = string
  description = "Value of the image to use."
  default     = "ubuntu_focal"
}

variable "instance_type" {
  type        = string
  description = "Instance type."
  validation {
    condition     = contains(["DEV1-M", "DEV1-L", "PLAY2-PICO"], var.instance_type)
    error_message = "Valid values for var: test_variable are (PLAY2-PICO, DEV1-M, DEV1-L)."
  }
}

variable "ssh_key_id" {
  type        = string
  description = "SSH key id."
}

variable "security_group_id" {
  type        = string
  description = "Security group id."
}
