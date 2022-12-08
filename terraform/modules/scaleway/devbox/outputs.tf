
output "id" {
  value       = scaleway_instance_server.devbox.id
  description = "The ID of the server."
}

output "placement_group_policy_respected" {
  value       = scaleway_instance_server.devbox.id
  description = "True when the placement group policy is respected."
}

output "root_volume_id" {
  value       = scaleway_instance_server.devbox.root_volume[0].volume_id
  description = "The volume ID of the root volume of the server."
}

output "private_ip" {
  value       = scaleway_instance_server.devbox.private_ip
  description = "The Scaleway internal IP addres of the server."
}

output "organization_id" {
  value       = scaleway_instance_server.devbox.organization_id
  description = "The organization ID the server is associated with."
}

output "ipv6_gateway" {
  value       = scaleway_instance_server.devbox.ipv6_gateway
  description = "The IPv6 gateway of the server."
}

output "ipv6" {
  value       = scaleway_instance_server.devbox.ipv6_address
  description = "The IPv6 address of the server."
}
