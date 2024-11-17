# Service account for Cloud Run
resource "google_service_account" "cloud_run_service_account" {
  account_id   = "cloud-run-service-account"
  display_name = "Cloud Run Service Account"
}

# Cloud Run service
resource "google_cloud_run_service" "default" {
  name     = "fuel-prices-agent-frontend"
  location = var.region

  metadata {
    annotations = {
      "run.googleapis.com/ingress"        = "internal-and-cloud-load-balancing"
      "run.googleapis.com/authentication" = "required"
    }
  }

  template {
    spec {
      service_account_name = google_service_account.cloud_run_service_account.email

      containers {
        image = var.image

        ports {
          container_port = 3000
        }
      }
    }
  }
}

# IAM policy to allow IAP to invoke the Cloud Run service
resource "google_cloud_run_service_iam_binding" "invoker" {
  location = var.region
  project  = var.project_id
  service  = google_cloud_run_service.default.name
  role     = "roles/run.invoker"
  members  = [
    "serviceAccount:service-${var.project_number}@gcp-sa-iap.iam.gserviceaccount.com"
  ]
}

# Serverless NEG for Cloud Run
resource "google_compute_region_network_endpoint_group" "default" {
  name                  = "cloud-run-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region

  cloud_run {
    service = google_cloud_run_service.default.name
  }
}

# Backend service with IAP enabled
resource "google_compute_backend_service" "default" {
  name                  = "backend-service"
  protocol              = "HTTPS"
  load_balancing_scheme = "EXTERNAL"

  backend {
    group = google_compute_region_network_endpoint_group.default.id
  }

  iap {
    enabled                      = true
    oauth2_client_id             = var.oauth2_client_id
    oauth2_client_secret         = var.oauth2_client_secret
    oauth2_client_secret_sha256  = var.oauth2_client_secret_sha256
  }
}

# URL map
resource "google_compute_url_map" "default" {
  name            = "url-map"
  default_service = google_compute_backend_service.default.self_link
}

# Managed SSL certificate
resource "google_compute_managed_ssl_certificate" "default" {
  name = "managed-ssl-cert"

  managed {
    domains = [var.domain]
  }
}

# Target HTTPS proxy
resource "google_compute_target_https_proxy" "default" {
  name               = "https-proxy"
  url_map            = google_compute_url_map.default.id
  ssl_certificates   = [google_compute_managed_ssl_certificate.default.id]
}

# Global forwarding rule
resource "google_compute_global_forwarding_rule" "default" {
  name        = "https-forwarding-rule"
  target      = google_compute_target_https_proxy.default.id
  port_range  = "443"
  ip_protocol = "TCP"
}
