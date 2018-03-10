# ~*~ coding: utf-8 ~*~

import os
from collections import namedtuple

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.playbook.play import Play
import ansible.constants as C

from  .callback import AdHocResultCallback, PlaybookResultCallBack, \
    CommandResultCallback
from  .exceptions import AnsibleError


__all__ = ["AdHocRunner", "PlayBookRunner"]
C.HOST_KEY_CHECKING = False



Options = namedtuple('Options', [
    'listtags', 'listtasks', 'listhosts', 'syntax', 'connection',
    'module_path', 'forks', 'remote_user', 'private_key_file', 'timeout',
    'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
    'scp_extra_args', 'become', 'become_method', 'become_user',
    'verbosity', 'check', 'extra_vars', 'playbook_path', 'passwords',
    'diff', 'gathering', 'remote_tmp',
])





def get_default_options():
    options = Options(
        listtags=False,
        listtasks=False,
        listhosts=False,
        syntax=False,
        timeout=60,
        connection='ssh',
        module_path='',
        forks=10,
        remote_user='root',
        private_key_file=None,
        ssh_common_args="",
        ssh_extra_args="",
        sftp_extra_args="",
        scp_extra_args="",
        become=None,
        become_method=None,
        become_user=None,
        verbosity=None,
        extra_vars=[],
        check=False,
        playbook_path='/etc/ansible/',
        passwords=None,
        diff=False,
        gathering='implicit',
        remote_tmp='/tmp/.ansible'
    )
    return options


# Jumpserver not use playbook
# class PlayBookRunner:
#     """
#     用于执行AnsiblePlaybook的接口.简化Playbook对象的使用.
#     """
#
#     # Default results callback
#     results_callback_class = PlaybookResultCallBack
#     loader_class = DataLoader
#     variable_manager_class = VariableManager
#     options = get_default_options()
#
#     def __init__(self, inventory=None, options=None):
#         """
#         :param options: Ansible options like ansible.cfg
#         :param inventory: Ansible inventory
#         """
#         if options:
#             self.options = options
#         C.RETRY_FILES_ENABLED = False
#         self.inventory = inventory
#         self.loader = self.loader_class()
#         self.results_callback = self.results_callback_class()
#         self.playbook_path = options.playbook_path
#         self.variable_manager = self.variable_manager_class(
#             loader=self.loader, inventory=self.inventory
#         )
#         self.passwords = options.passwords
#         self.__check()
#
#     def __check(self):
#         if self.options.playbook_path is None or \
#                 not os.path.exists(self.options.playbook_path):
#             raise AnsibleError(
#                 "Not Found the playbook file: {}.".format(self.options.playbook_path)
#             )
#         if not self.inventory.list_hosts('all'):
#             raise AnsibleError('Inventory is empty')
#
#     def run(self):
#         executor = PlaybookExecutor(
#             playbooks=[self.playbook_path],
#             inventory=self.inventory,
#             variable_manager=self.variable_manager,
#             loader=self.loader,
#             options=self.options,
#             passwords=self.passwords
#         )
#
#         if executor._tqm:
#             executor._tqm._stdout_callback = self.results_callback
#         executor.run()
#         executor._tqm.cleanup()
#         return self.results_callback.output




##此方法为别人测试给我的，我暂无测试。 应该可以用。
class PlayBookRunner:


        def __init__(self, playbook_path, inventory=None, options=None):
            """
            :param options: Ansible options like ansible.cfg
            :param inventory: Ansible inventory
            :param BaseInventory:The BaseInventory parameter hostname must be equal to the hosts in yaml
            or the BaseInventory parameter groups must equal to the hosts in yaml.
            """
            if options:
                self.options = options
            C.RETRY_FILES_ENABLED = False
            self.inventory = inventory
            # self.loader = self.loader_class()
            self.loader = DataLoader()
            self.results_callback = self.results_callback_class()
            # self.playbook_path = options.playbook_path
            self.playbook_path = playbook_path
            self.variable_manager = self.variable_manager_class(
                loader=self.loader, inventory=self.inventory
            )
            # self.passwords = options.passwords
            self.passwords = {"passwords":''}#为了修改paramiko中的bug添加入，无实际意义
            self.__check()

        def __check(self):
            if self.options.playbook_path is None or \
                    not os.path.exists(self.options.playbook_path):
                raise AnsibleError(
                    "Not Found the playbook file: {}.".format(self.options.playbook_path)
                )
            if not self.inventory.list_hosts('all'):
                raise AnsibleError('Inventory is empty')

        def run(self):
            executor = PlaybookExecutor(
                playbooks=[self.playbook_path],
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords
            )

            if executor._tqm:
                executor._tqm._stdout_callback = self.results_callback
            executor.run()
            executor._tqm.cleanup()
            try:
                results_callback=self.results_callback.output['plays'][0]['tasks'][1]['hosts']
                status=self.results_callback.output['stats']
                results={"results_callback":results_callback,"status":status}
                return results
            except Exception as e:
                raise AnsibleError('The hostname parameter or groups parameter in the BaseInventory \
                                   does not match the hosts parameter in the yaml file.')








class AdHocRunner:
    """
    ADHoc Runner接口
    """
    results_callback_class = AdHocResultCallback
    loader_class = DataLoader
    variable_manager_class = VariableManager
    options = get_default_options()
    default_options = get_default_options()

    def __init__(self, inventory, options=None):
        if options:
            self.options = options
        self.inventory = inventory
        self.loader = DataLoader()
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory
        )

    @staticmethod
    def check_module_args(module_name, module_args=''):
        if module_name in C.MODULE_REQUIRE_ARGS and not module_args:
            err = "No argument passed to '%s' module." % module_name
            raise AnsibleError(err)

    def check_pattern(self, pattern):
        if not pattern:
            raise AnsibleError("Pattern `{}` is not valid!".format(pattern))
        if not self.inventory.list_hosts("all"):
            raise AnsibleError("Inventory is empty.")
        if not self.inventory.list_hosts(pattern):
            raise AnsibleError(
                "pattern: %s  dose not match any hosts." % pattern
            )

    def clean_tasks(self, tasks):
        cleaned_tasks = []
        for task in tasks:
            self.check_module_args(task['action']['module'], task['action'].get('args'))
            cleaned_tasks.append(task)
        return cleaned_tasks

    def set_option(self, k, v):
        kwargs = {k: v}
        self.options = self.options._replace(**kwargs)

    def run(self, tasks, pattern, play_name='Ansible Ad-hoc', gather_facts='no'):
        """
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
            options=self.options,
            stdout_callback=results_callback,
            passwords=self.options.passwords,
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
            raise AnsibleError("Module should in {}".format(self.modules_choices))
        else:
            module = "shell"

        tasks = [
            {"action": {"module": module, "args": cmd}}
        ]
        hosts = self.inventory.get_hosts(pattern=pattern)
        name = "Run command {} on {}".format(cmd, ", ".join([host.name for host in hosts]))
        return self.run(tasks, pattern, play_name=name)

