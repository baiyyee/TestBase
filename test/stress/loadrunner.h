#include "web_api.h"


Action()
{
	
	int HttpRetCode;
	                                     
	lr_start_transaction("send_request");

	web_custom_request("send_request", 
        "URL=https://cn.bing.com/?FORM=Z9FD1",
		"Method=GET",
		LAST);

        HttpRetCode = web_get_int_property(HTTP_INFO_RETURN_CODE);

	if(HttpRetCode == 200){
        lr_end_transaction("send_request", LR_PASS);
	}
	
	return 0;
}