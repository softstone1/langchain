from kubernetes import client, config
import logging

# Configure logging for the module
logger = logging.getLogger(__name__)

# Load local kubeconfig for now; modify for in-cluster config as needed
config.load_kube_config()

def list_pods_with_errors(namespace):
    try:
        v1 = client.CoreV1Api()
        pods = v1.list_namespaced_pod(namespace)
        error_pods = [pod.metadata.name for pod in pods.items if any(
            cs.state.waiting and cs.state.waiting.reason != 'ContainerCreating'
            for cs in (pod.status.container_statuses or [])
        )]
        return error_pods
    except Exception as e:
        logger.error(f"Error listing pods in namespace {namespace}: {e}")
        raise
