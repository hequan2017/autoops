from django.test import TestCase
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest



client = AcsClient(
       "LTAIs0cvr1vbZoBT",
       "MOw73YeLQpjWuybIchdMUk5WVnEecb",
       "cn-beijing"
   );

request = DescribeInstancesRequest.DescribeInstancesRequest()
request.set_PageSize(10)
response = client.do_action_with_exception(request)
print(response)


