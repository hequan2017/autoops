from  django import  template
##自定义过滤器
register = template.Library()


@register.filter
def	 lowers(text):
	a = text.split("/")
	b = a[-1]
	return	  b




