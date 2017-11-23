from django.test import TestCase

# Create your tests here.
a = "%Cpu(s):  2.1 us,  1.0 sy,  0.0 ni, 96.7 id,  0.2 wa,  0.0 hi,  0.0 si,  0.0 st"
cpu2 = a.split()
print(cpu2)
cpu3 = cpu2[1].split('%')
cpu4= cpu2[3].split('%')

cpu5 = float(str(cpu3[0]))+float(str(cpu4[0]))


print(cpu5)