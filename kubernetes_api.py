import os
import shutil
from kubernetes import client, config
from kubernetes.stream import stream


class KubernetesAPI:
    def __init__(self):
        # Load Kubernetes configuration
        config.load_kube_config()

        # List all pods in the cluster
        self.v1 = client.CoreV1Api()
        self.pod_list = self.v1.list_pod_for_all_namespaces(watch=False)

    def get_user_pods(self):
        pods = []
        for pod in self.pod_list.items:
            # Check if the pod name starts with 'jupyter'
            if pod.metadata.name.startswith('jupyter-'):
                pods.append(pod)

        return pods

    def copy_file(self, source_path: str, dest_path: str, recursive: bool = False):
        user_pods = self.get_user_pods()
        for pod in user_pods:
            # Copy the file to the pod
            command = ['cp', source_path, f'{pod.metadata.name}:{dest_path}']
            if recursive:
                command.insert(1, '-r')

            resp = stream(
                self.v1.connect_get_namespaced_pod_exec,
                pod.metadata.name,
                pod.metadata.namespace,
                command=command,
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False,
            )

            # Check if the file was copied successfully
            # if resp.exit_code == 0:
            #     print(f"File copied to {pod.metadata.name}")
            # else:
            #     print(f"Failed to copy file to {pod.metadata.name}")
