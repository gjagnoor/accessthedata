locals {
  // General Variables
  project_name = "access-the-data"
  environment  = "dev"

  // ALB
  aws_managed_dns = false
  host_names      = [""]
  path_patterns   = ["/*"] 

  // ECS
  application_type = "fullstack"
  launch_type      = "FARGATE"

  // RDS (Database)
  postgres_database = {
    // no RDS credentials here
    // this is only for creating a new db 
  }

  // Container variables
  container_image   = "1234567.dkr.ecr.us-west-2.amazonaws.com/civictechjobs-fullstack-stage:latest" 
  desired_count     = 1
  container_port    = 8000 // should match server used by application 
  container_memory  = 512
  container_cpu     = 256
  health_check_path = "/"

  container_env_vars = {
    // key : value 
    // any env variables necessary for the docker container_image
    // RDS info here
  }
}