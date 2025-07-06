variable "bq_dataset_name" {
  description = "My BigQuery Dataset"
  default = "demo_dataset"
}

variable "gcs_bucket_n" {
  description = "My Storage"
  default = "demo_dataset"
}

variable "gcs_storage_c" {
  description = "Bucket Storage Class"
  default = "STANDARD"
}

variable "location" {
  description = "Project Location"
  default = "US"
}