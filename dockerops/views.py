from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages

import docker


class DockerContainerList(View):
    template_name = 'dockerops/containers.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DockerContainerList, self).dispatch(*args, **kwargs)

    def _get_client(self):
        return docker.from_env()

    def _get_containers(self, client):
        return client.containers.list(all=True)

    def _format_ports(self, ports):
        if not ports:
            return ['-']
        formatted = []
        for port, bindings in ports.items():
            if not bindings:
                formatted.append(port)
                continue
            host_bindings = []
            for binding in bindings:
                host_ip = binding.get('HostIp', '')
                host_port = binding.get('HostPort', '')
                host_bindings.append(f"{host_ip}:{host_port}".strip(':'))
            formatted.append(f"{port} -> {', '.join(host_bindings)}")
        return formatted

    def _serialize_containers(self, containers):
        serialized = []
        for container in containers:
            attrs = container.attrs or {}
            config = attrs.get('Config', {})
            serialized.append({
                'id': container.id,
                'name': container.name,
                'image': ', '.join(container.image.tags) if container.image.tags else container.image.short_id,
                'status': container.status,
                'created': attrs.get('Created', ''),
                'command': ' '.join(config.get('Cmd') or []),
                'ports': self._format_ports(attrs.get('NetworkSettings', {}).get('Ports')),
            })
        return serialized

    def get(self, request):
        try:
            client = self._get_client()
            containers = self._serialize_containers(self._get_containers(client))
            error_message = None
        except docker.errors.DockerException as exc:
            containers = []
            error_message = str(exc)

        context = {
            'docker_active': 'active',
            'docker_list_active': 'active',
            'containers': containers,
            'error_message': error_message,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        container_id = request.POST.get('container_id')
        action = request.POST.get('action')
        if not container_id or action not in {'start', 'stop', 'restart'}:
            messages.error(request, '无效的容器操作请求。')
            return redirect('dockerops:container_list')

        try:
            client = self._get_client()
            container = client.containers.get(container_id)
            if action == 'start':
                container.start()
                messages.success(request, '容器已启动。')
            elif action == 'stop':
                container.stop()
                messages.success(request, '容器已停止。')
            elif action == 'restart':
                container.restart()
                messages.success(request, '容器已重启。')
        except docker.errors.DockerException as exc:
            messages.error(request, f'容器操作失败: {exc}')

        return redirect('dockerops:container_list')
