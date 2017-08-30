from	django	import	forms

class	PublisherForm(forms.Form):
	network_ip = forms.GenericIPAddressField(label='外网IP')
	manage_ip = forms.GenericIPAddressField(label='管理IP')
	model = forms.CharField(max_length=64, label='型号')
	data_center = forms.CharField(label='数据中心',max_length=64,)
	cabinet =forms.CharField(max_length=64, label='机柜', )
	position = forms.CharField(max_length=64, label='位置')
	sn = forms.CharField(max_length=64, label='序列号')
	cpu = forms.CharField(max_length=64, label='CPU')
	memory = forms.CharField(max_length=64, label='内存')
	disk = forms.CharField(max_length=256, label="硬盘")
	port = forms.CharField(max_length=256, label="上联端口")
	use = forms.BooleanField(label='是否在用')
	
	ship_time =  forms.DateField(label="出厂时间")
	end_time =  forms.DateField(label="到保时间")
	product_line =  forms.CharField(max_length=64, label='产品线')
	
	ps =  forms.CharField(max_length=1024, label="备注")

