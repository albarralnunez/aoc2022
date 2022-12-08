output "naming" {
  description = "Naming convention."

  value = {
    Name        = join("-", [var.environment, var.project_name, var.project_component])
    Environment = var.environment
    Project     = var.project_name
    Component   = var.project_component
    Region      = var.region
  }
}

output "tags" {
  description = "Tags."

  value = {
    Region      = var.region
    Environment = var.environment
    Project     = var.project_name
    Component   = var.project_component
  }
}
