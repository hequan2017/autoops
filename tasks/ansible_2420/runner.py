# ~*~ coding: utf-8 ~*~

import os

from ansible import context
import ansible.constants as C
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.module_utils.common.collections import ImmutableDict
from ansible.playbook.play import Play
try:
    # ansible-core 2.15+ 需要显式初始化插件加载器
    from ansible.plugins.loader import init_plugin_loader
except ImportError:  # 兼容旧版 ansible-core
    init_plugin_loader = None

from .callback import AdHocResultCallback, PlaybookResultCallBack, \
    CommandResultCallback
from .exceptions import AnsibleError


__all__ = ["AdHocRunner", "PlayBookRunner"]
C.HOST_KEY_CHECKING = False


def get_default_options():
    """与 ansible CLI 等价的默认参数。

    ansible-core 2.10+ 移除了 Options namedtuple 传参方式，
    统一通过 context.CLIARGS（ImmutableDict）读取配置。
    """
    return ImmutableDict(
        listtags=False,
        listtasks=False,
        listhosts=False,
        syntax=False,
        timeout=60,
        connection='ssh',
        module_path='',
        forks=20,
        remote_user='root',
        private_key_file=None,
        ssh_common_args="",
        ssh_extra_args="",
        sftp_extra_args="",
        scp_extra_args="",
        become=False,
        become_method=None,
        become_user=None,
        verbosity=0,
        extra_vars={},
        check=False,
        playbook_path='/etc/ansible/',
        passwords=None,
        diff=False,
        gathering='implicit',
        remote_tmp='/tmp/.ansible',
    )

#  执行 yml 文件


class PlayBookRunner:

    # Default results callback
    results_callback_class = PlaybookResultCallBack
    loader_class = DataLoader
    variable_manager_class = VariableManager

    def __init__(self, playbook_path, inventory=None, options=None):
        """
        :param options: Ansible options like ansible.cfg
        :param inventory: Ansible inventory
        :param BaseInventory:The BaseInventory parameter hostname must be equal to the hosts in yaml
        or the BaseInventory parameter groups must equal to the hosts in yaml.
        """
        if init_plugin_loader:
            init_plugin_loader()
        context._init_global_context(options or get_default_options())
        C.RETRY_FILES_ENABLED = False
        self.inventory = inventory
        self.loader = DataLoader()
        self.results_callback = self.results_callback_class()
        self.playbook_path = playbook_path
        self.variable_manager = self.variable_manager_class(
            loader=self.loader, inventory=self.inventory
        )
        # self.passwords = options.passwords
        self.passwords = {"passwords": ''}  # 为了修改paramiko中的bug添加入，无实际意义
        self.__check()

    def __check(self):
        if self.playbook_path is None or \
                not os.path.exists(self.playbook_path):
            raise AnsibleError(
                "Not Found the playbook file: " + str(self.playbook_path) + ".")
        if not self.inventory.list_hosts('all'):
            raise AnsibleError('Inventory is empty')

    def run(self):
        executor = PlaybookExecutor(
            playbooks=[self.playbook_path],
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            passwords=self.passwords
        )

        if executor._tqm:
            executor._tqm._stdout_callback = self.results_callback
        executor.run()
        executor._tqm.cleanup()
        try:
            results_callback = self.results_callback.output['plays'][0]['tasks'][1]['hosts']
            status = self.results_callback.output['stats']
            results = {"results_callback": results_callback, "status": status}
            return results
        except Exception as e:

            raise AnsibleError(
                'The hostname parameter or groups parameter in the BaseInventory \
                               does not match the hosts parameter in the yaml file.' + str(e))


class AdHocRunner:
    """
    ADHoc Runner接口
    """
    results_callback_class = AdHocResultCallback
    loader_class = DataLoader
    variable_manager_class = VariableManager

    def __init__(self, inventory, options=None):
        if init_plugin_loader:
            init_plugin_loader()
        context._init_global_context(options or get_default_options())
        self.inventory = inventory
        self.loader = DataLoader()
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory
        )

    @staticmethod
    def check_module_args(module_name, module_args=''):
        if module_name in C.MODULE_REQUIRE_ARGS and not module_args:
            err = "No argument passed to '" + str(module_name) + "' module."
            raise AnsibleError(err)

    def check_pattern(self, pattern):
        if not pattern:
            raise AnsibleError("Pattern `" + str(pattern) + "` is not valid!")
        if not self.inventory.list_hosts("all"):
            raise AnsibleError("Inventory is empty.")
        if not self.inventory.list_hosts(pattern):
            raise AnsibleError(
                "pattern: " + str(pattern) + "  dose not match any hosts."
            )

    def clean_tasks(self, tasks):
        cleaned_tasks = []
        for task in tasks:
            self.check_module_args(
                task['action']['module'],
                task['action'].get('args'))
            cleaned_tasks.append(task)
        return cleaned_tasks

    def run(
            self,
            tasks,
            pattern,
            play_name='Ansible Ad-hoc',
            gather_facts='no',):
        """
        :param gather_facts:
        :param tasks: [{'action': {'module': 'shell', 'args': 'ls'}, ...}, ]
        :param pattern: all, *, or others
        :param play_name: The play name
        :return:
        """
        self.check_pattern(pattern)
        results_callback = self.results_callback_class()
        cleaned_tasks = self.clean_tasks(tasks)

        play_source = dict(
            name=play_name,
            hosts=pattern,
            gather_facts=gather_facts,
            tasks=cleaned_tasks
        )

        play = Play().load(
            play_source,
            variable_manager=self.variable_manager,
            loader=self.loader,
        )

        tqm = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            stdout_callback=results_callback,
            passwords=self.passwords,
        )

        try:
            tqm.run(play)
            return results_callback
        except Exception as e:
            raise AnsibleError(e)
        finally:
            tqm.cleanup()
            self.loader.cleanup_all_tmp_files()


class CommandRunner(AdHocRunner):
    results_callback_class = CommandResultCallback
    modules_choices = ('shell', 'raw', 'command', 'script')

    def execute(self, cmd, pattern, module=None):
        if module and module not in self.modules_choices:
            raise AnsibleError("Module should in " + str(self.modules_choices))
        else:
            module = "shell"

        tasks = [
            {"action": {"module": module, "args": cmd}}
        ]
        hosts = self.inventory.get_hosts(pattern=pattern)
        name = "Run command " + str(cmd) + " on " + ", ".join([host.name for host in hosts])
        return self.run(tasks, pattern, play_name=name)
