terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.42.0"
    }
  }
}

provider "google" {
  project = "fleet-muse-464901-m2"
  region  = "us-central1"
}

resource "google_storage_bucket" "auto-expire" {
  name          = var.gcs_bucket_n
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
  location = var.location
}