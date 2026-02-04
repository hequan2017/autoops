from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException


class KubernetesOverview(View):
    template_name = 'k8sops/overview.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(KubernetesOverview, self).dispatch(*args, **kwargs)

    def _load_config(self):
        try:
            config.load_kube_config()
        except ConfigException:
            config.load_incluster_config()

    def _list_items(self, list_fn, item_builder):
        return [item_builder(item) for item in list_fn().items]

    def get(self, request):
        error_message = None
        data = {}
        try:
            self._load_config()
            core_api = client.CoreV1Api()
            apps_api = client.AppsV1Api()
            batch_api = client.BatchV1Api()

            data['namespaces'] = self._list_items(
                core_api.list_namespace,
                lambda ns: {
                    'name': ns.metadata.name,
                    'status': ns.status.phase,
                },
            )
            data['nodes'] = self._list_items(
                core_api.list_node,
                lambda node: {
                    'name': node.metadata.name,
                    'status': next(
                        (condition.type for condition in node.status.conditions or []
                         if condition.status == 'True'),
                        'Unknown',
                    ),
                    'version': node.status.node_info.kubelet_version,
                },
            )
            data['pods'] = self._list_items(
                core_api.list_pod_for_all_namespaces,
                lambda pod: {
                    'name': pod.metadata.name,
                    'namespace': pod.metadata.namespace,
                    'status': pod.status.phase,
                    'node': pod.spec.node_name,
                },
            )
            data['services'] = self._list_items(
                core_api.list_service_for_all_namespaces,
                lambda svc: {
                    'name': svc.metadata.name,
                    'namespace': svc.metadata.namespace,
                    'type': svc.spec.type,
                    'cluster_ip': svc.spec.cluster_ip,
                },
            )
            data['configmaps'] = self._list_items(
                core_api.list_config_map_for_all_namespaces,
                lambda cm: {
                    'name': cm.metadata.name,
                    'namespace': cm.metadata.namespace,
                },
            )
            data['secrets'] = self._list_items(
                core_api.list_secret_for_all_namespaces,
                lambda secret: {
                    'name': secret.metadata.name,
                    'namespace': secret.metadata.namespace,
                    'type': secret.type,
                },
            )
            data['deployments'] = self._list_items(
                apps_api.list_deployment_for_all_namespaces,
                lambda dep: {
                    'name': dep.metadata.name,
                    'namespace': dep.metadata.namespace,
                    'replicas': dep.status.ready_replicas or 0,
                    'desired': dep.spec.replicas or 0,
                },
            )
            data['daemonsets'] = self._list_items(
                apps_api.list_daemon_set_for_all_namespaces,
                lambda ds: {
                    'name': ds.metadata.name,
                    'namespace': ds.metadata.namespace,
                    'desired': ds.status.desired_number_scheduled,
                    'ready': ds.status.number_ready,
                },
            )
            data['statefulsets'] = self._list_items(
                apps_api.list_stateful_set_for_all_namespaces,
                lambda sts: {
                    'name': sts.metadata.name,
                    'namespace': sts.metadata.namespace,
                    'ready': sts.status.ready_replicas or 0,
                    'desired': sts.spec.replicas or 0,
                },
            )
            data['jobs'] = self._list_items(
                batch_api.list_job_for_all_namespaces,
                lambda job: {
                    'name': job.metadata.name,
                    'namespace': job.metadata.namespace,
                    'succeeded': job.status.succeeded or 0,
                    'failed': job.status.failed or 0,
                },
            )
            data['cronjobs'] = self._list_items(
                batch_api.list_cron_job_for_all_namespaces,
                lambda cj: {
                    'name': cj.metadata.name,
                    'namespace': cj.metadata.namespace,
                    'schedule': cj.spec.schedule,
                },
            )
        except Exception as exc:
            error_message = str(exc)
            data = {
                'namespaces': [],
                'nodes': [],
                'pods': [],
                'services': [],
                'configmaps': [],
                'secrets': [],
                'deployments': [],
                'daemonsets': [],
                'statefulsets': [],
                'jobs': [],
                'cronjobs': [],
            }

        context = {
            'k8s_active': 'active',
            'k8s_overview_active': 'active',
            'error_message': error_message,
            **data,
        }
        return render(request, self.template_name, context)
