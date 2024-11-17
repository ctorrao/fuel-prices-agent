variable "project_id" {
  description = "Google Cloud project ID"
}

variable "project_number" {
  description = "Google Cloud project number"
}

variable "region" {
  description = "Google Cloud region"
  default     = "us-central1"
}

variable "image" {
  description = "Docker image to be deployed"
}

variable "domain" {
  description = "Domain for the SSL certificate"
}

variable "oauth2_client_id" {
  description = "OAuth2 Client ID for IAP"
}

variable "oauth2_client_secret" {
  description = "OAuth2 Client Secret for IAP"
  sensitive   = true
}

variable "oauth2_client_secret_sha256" {
  description = "SHA256 hash of the OAuth2 Client Secret"
}