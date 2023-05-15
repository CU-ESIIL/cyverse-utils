import os
import subprocess


def add_github_to_known_hosts():
    known_hosts_file = os.path.expanduser('~/.ssh/known_hosts')
    host = 'github.com'

    # Create known_hosts file if it doesn't exist
    # subprocess.run(['touch', known_hosts_file])

    # Retrieve the host key using ssh-keyscan
    output = subprocess.run(['ssh-keyscan', '-t', 'rsa', host], capture_output=True, text=True)
    host_key = output.stdout.strip()

    # Append the host key to the known hosts file
    with open(known_hosts_file, 'a') as file:
        file.write(host_key + '\n')

    print(f'{host} added to known hosts file.')


def configure():
    username = input('GitHub username:')
    email = input('GitHub email:')

    subprocess.run(["git", "config", "--global", "user.name", username])
    subprocess.run(["git", "config", "--global", "user.email", email])

    # Generate Ed25519 keypair
    ssh_dir = os.path.expanduser("~/.ssh")
    key_name = "github"
    private_key_path = os.path.join(ssh_dir, key_name)
    public_key_path = private_key_path + ".pub"

    subprocess.run(["ssh-keygen", "-t", "ed25519", "-f", private_key_path, "-N", ""])

    # Update SSH config
    config_file = os.path.join(ssh_dir, "config")
    github_config = f"""
    Host github.com
        HostName github.com
        IdentityFile {private_key_path}
    """

    with open(config_file, "a") as file:
        file.write(github_config)

    # Print public key
    with open(public_key_path, "r") as file:
        public_key = file.read()

    subprocess.run(["eval", "$(ssh-agent -s)", "&&", "ssh-add", private_key_path], shell=True)

    add_github_to_known_hosts()

    print("Public Key:")
    print(public_key)
