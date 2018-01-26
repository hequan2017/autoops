
a = "%d" % 22
print(a)

from  multiprocessing  import   current_process

a = current_process()._config
print(type(a))
print(dir(a))
