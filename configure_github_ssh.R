# Install the processx package if not already installed
if (!requireNamespace("processx", quietly = TRUE)) {
  install.packages("processx")
}
library(processx)

# Function to add GitHub to known hosts
add_github_to_known_hosts <- function() {
  known_hosts_file <- path.expand("~/.ssh/known_hosts")
  host <- "github.com"

  # Retrieve the host key using ssh-keyscan
  host_key <- system2("ssh-keyscan", args = c("-t", "rsa", host), stdout = TRUE)

  # Append the host key to the known hosts file
  cat(host_key, file = known_hosts_file, append = TRUE)

  cat(paste0(host, " added to known hosts file.\n"))
}

# Main configuration function
configure <- function() {
  username <- readline(prompt = "GitHub username: ")
  email <- readline(prompt = "GitHub email: ")

  system2("git", args = c("config", "--global", "user.name", username))
  system2("git", args = c("config", "--global", "user.email", email))
    
  # Define the path to the .ssh directory in the user's home directory
  ssh_dir <- file.path(Sys.getenv("HOME"), ".ssh")

  # Check if the directory exists, and if not, create it
  if (!dir.exists(ssh_dir)) {
    dir.create(ssh_dir, recursive = TRUE)
  }

  # Generate Ed25519 keypair
  key_name <- "github"
  private_key_path <- file.path(ssh_dir, key_name)
  public_key_path <- paste0(private_key_path, ".pub")

  system2("ssh-keygen", args = c("-t", "ed25519", "-f", private_key_path, "-N", '""'))

  # Update SSH config
  config_file <- file.path(ssh_dir, "config")
  github_config <- sprintf("
Host github.com
    HostName github.com
    IdentityFile %s
", private_key_path)

  cat(github_config, file = config_file, append = TRUE)

  # Print public key
  public_key <- readLines(public_key_path)
  cat("Public Key:\n")
  cat(public_key, sep = "\n")

  # Add GitHub to known hosts
  add_github_to_known_hosts()
}

# Run the configuration
configure()
