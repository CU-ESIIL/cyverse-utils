from kubernetes import client, config
import subprocess as sp


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
            command = ['kubectl', 'cp', source_path, f'{pod.metadata.name}:{dest_path}']
            if recursive:
                command.insert(1, '-r')
            sp.call(command)
