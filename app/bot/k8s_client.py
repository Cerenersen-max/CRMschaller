"""Not: '/scale up, /deploy prod gibi komutlar ile yonetim ... K8s API'ye
baglanir.' Telegram botunun kullandigi ince Kubernetes istemcisi."""
from __future__ import annotations

from kubernetes import client, config

from app.config import get_settings


class K8sClient:
    def __init__(self) -> None:
        settings = get_settings()
        try:
            if settings.kube_config_path:
                config.load_kube_config(config_file=settings.kube_config_path)
            else:
                config.load_incluster_config()
            self._connected = True
        except Exception:  # noqa: BLE001 - cluster disinda calisirken sessizce dry-run'a dus
            self._connected = False
        self.namespace = settings.kube_namespace
        self._apps_api = client.AppsV1Api() if self._connected else None
        self._core_api = client.CoreV1Api() if self._connected else None

    @property
    def connected(self) -> bool:
        return self._connected

    def status(self) -> str:
        if not self._connected:
            return "K8s API'ye baglanilamadi (KUBE_CONFIG_PATH ayarli mi kontrol edin)."
        deployments = self._apps_api.list_namespaced_deployment(self.namespace)
        lines = [
            f"{d.metadata.name}: {d.status.ready_replicas or 0}/{d.spec.replicas} hazir"
            for d in deployments.items
        ]
        return "\n".join(lines) or "Namespace icinde deployment bulunamadi."

    def logs(self, deployment_name: str, tail_lines: int = 100) -> str:
        if not self._connected:
            return "K8s API'ye baglanilamadi."
        pods = self._core_api.list_namespaced_pod(
            self.namespace, label_selector=f"app={deployment_name}"
        )
        if not pods.items:
            return f"'{deployment_name}' icin pod bulunamadi."
        pod_name = pods.items[0].metadata.name
        return self._core_api.read_namespaced_pod_log(
            name=pod_name, namespace=self.namespace, tail_lines=tail_lines
        )

    def scale(self, deployment_name: str, replicas: int) -> str:
        if not self._connected:
            return "K8s API'ye baglanilamadi."
        self._apps_api.patch_namespaced_deployment_scale(
            name=deployment_name,
            namespace=self.namespace,
            body={"spec": {"replicas": replicas}},
        )
        return f"'{deployment_name}' {replicas} replikaya olceklendi."

    def deploy(self, deployment_name: str, image: str) -> str:
        if not self._connected:
            return "K8s API'ye baglanilamadi."
        self._apps_api.patch_namespaced_deployment(
            name=deployment_name,
            namespace=self.namespace,
            body={
                "spec": {
                    "template": {
                        "spec": {"containers": [{"name": deployment_name, "image": image}]}
                    }
                }
            },
        )
        return f"'{deployment_name}' icin '{image}' imaji dagitildi (prod)."
