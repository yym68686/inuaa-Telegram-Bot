# _VAR_ADDR
# _VAR_TODAY
# ORGANIZES_Codes
# stepId, fieldAfdy, timestamp, jsessionID, csrfToken, leaveSchool_timestamp, Studept
import re

result = '''
POST /infoplus/interface/doAction HTTP/1.1
Host: ehall.nuaa.edu.cn
Cookie: INGRESSCOOKIE=1668072316.966.605.828667; JSESSIONID=87ED18A6EF06DD6586E56E57A9A921C2.tomcat-infoplus-0; iPlanetDirectoryPro=boI7BmH4diqUWNG0THIqJK1xJZTDqQSr
Content-Length: 6651
Sec-Ch-Ua: "Not;A=Brand";v="99", "Chromium";v="106"
Accept: application/json, text/javascript, */*; q=0.01
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36
Sec-Ch-Ua-Platform: "macOS"
Origin: https://ehall.nuaa.edu.cn
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://ehall.nuaa.edu.cn/infoplus/form/19894858/render?theme=nuaa_new
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

actionId=20&formData=%7B%22_VAR_EXECUTE_INDEP_ORGANIZE_Name%22%3A%22%E9%95%BF%E7%A9%BA%E5%AD%A6%E9%99%A2%22%2C%22_VAR_ACTION_ACCOUNT%22%3A%22161910229%22%2C%22_VAR_ACTION_INDEP_ORGANIZES_Codes%22%3A%220518000%22%2C%22_VAR_ACTION_REALNAME%22%3A%22%E5%BC%A0%E7%82%80%22%2C%22_VAR_ACTION_INDEP_ORGANIZES_Names%22%3A%22%E9%95%BF%E7%A9%BA%E5%AD%A6%E9%99%A2%22%2C%22_VAR_OWNER_ACCOUNT%22%3A%22161910229%22%2C%22_VAR_ACTION_ORGANIZES_Names%22%3A%22%E9%95%BF%E7%A9%BA%E5%AD%A6%E9%99%A2%22%2C%22_VAR_STEP_CODE%22%3A%22SQR%22%2C%22_VAR_ACTION_ORGANIZE%22%3A%220518000%22%2C%22_VAR_OWNER_PHONE%22%3A%2215862949119%22%2C%22_VAR_OWNER_USERCODES%22%3A%22161910229%22%2C%22_VAR_EXECUTE_ORGANIZE%22%3A%220518000%22%2C%22_VAR_EXECUTE_ORGANIZES_Codes%22%3A%220518000%22%2C%22_VAR_NOW_DAY%22%3A%2210%22%2C%22_VAR_ACTION_INDEP_ORGANIZE%22%3A%220518000%22%2C%22_VAR_OWNER_REALNAME%22%3A%22%E5%BC%A0%E7%82%80%22%2C%22_VAR_ENTRY_TAGS%22%3A%2201-%E7%96%AB%E6%83%85%E9%98%B2%E6%8E%A7%E6%9C%8D%E5%8A%A1%2C%E7%A7%BB%E5%8A%A8%E7%AB%AF%22%2C%22_VAR_ACTION_INDEP_ORGANIZE_Name%22%3A%22%E9%95%BF%E7%A9%BA%E5%AD%A6%E9%99%A2%22%2C%22_VAR_NOW%22%3A%221668072325%22%2C%22_VAR_ACTION_ORGANIZE_Name%22%3A%22%E9%95%BF%E7%A9%BA%E5%AD%A6%E9%99%A2%22%2C%22_VAR_EXECUTE_ORGANIZES_Names%22%3A%22%E9%95%BF%E7%A9%BA%E5%AD%A6%E9%99%A2%22%2C%22_VAR_OWNER_ORGANIZES_Codes%22%3A%220518000%22%2C%22_VAR_ADDR%22%3A%2210.100.219.184%22%2C%22_VAR_URL_Attr%22%3A%22%7B%5C%22theme%5C%22%3A%5C%22nuaa_new%5C%22%7D%22%2C%22_VAR_ENTRY_NUMBER%22%3A%2214582484%22%2C%22_VAR_OWNER_ACCOUNT_FRIENDLY%22%3A%22161910229%22%2C%22_VAR_EXECUTE_INDEP_ORGANIZES_Names%22%3A%22%E9%95%BF%E7%A9%BA%E5%AD%A6%E9%99%A2%22%2C%22_VAR_ENTRY_NAME%22%3A%22_%E7%96%AB%E6%83%85%E9%98%B2%E6%8E%A7%E6%9C%9F%E5%AD%A6%E7%94%9F%E9%9B%B6%E6%98%9F%E8%BF%9B%E5%87%BA%E6%A0%A1%E7%94%B3%E8%AF%B7%22%2C%22_VAR_EXECUTE_USERCODES%22%3A%22161910229%22%2C%22_VAR_STEP_NUMBER%22%3A%2219894858%22%2C%22_VAR_POSITIONS%22%3A%220518000%3A11%3A161910229%22%2C%22_VAR_ACTION_PHONE%22%3A%2215862949119%22%2C%22_VAR_OWNER_ORGANIZES_Names%22%3A%22%E9%95%BF%E7%A9%BA%E5%AD%A6%E9%99%A2%22%2C%22_VAR_URL%22%3A%22https%3A%2F%2Fehall.nuaa.edu.cn%2Finfoplus%2Fform%2F19894858%2Frender%3Ftheme%3Dnuaa_new%22%2C%22_VAR_EXECUTE_ORGANIZE_Name%22%3A%22%E9%95%BF%E7%A9%BA%E5%AD%A6%E9%99%A2%22%2C%22_VAR_EXECUTE_INDEP_ORGANIZES_Codes%22%3A%220518000%22%2C%22_VAR_RELEASE%22%3A%22true%22%2C%22_VAR_EXECUTE_POSITIONS%22%3A%220518000%3A11%3A161910229%22%2C%22_VAR_TODAY%22%3A%221668009600%22%2C%22_VAR_NOW_MONTH%22%3A%2211%22%2C%22_VAR_ACTION_USERCODES%22%3A%22161910229%22%2C%22_VAR_ACTION_ORGANIZES_Codes%22%3A%220518000%22%2C%22_VAR_URL_Name%22%3A%22https%3A%2F%2Fehall.nuaa.edu.cn%2Finfoplus%2Fform%2FYQFKXSFXLSCX_CS%2Fstart%3Ftheme%3Dnuaa_new%22%2C%22_VAR_EXECUTE_INDEP_ORGANIZE%22%3A%220518000%22%2C%22_VAR_NOW_YEAR%22%3A%222022%22%2C%22_VAR_ACTION_ACCOUNT_FRIENDLY%22%3A%22161910229%22%2C%22groupQWDDList%22%3A%5B0%5D%2C%22fieldHMDFZ%22%3A%221%22%2C%22fieldXSSF%22%3A%22%E6%9C%AC%E7%A7%91%E7%94%9F%22%2C%22fieldSQSJ%22%3A1668072325%2C%22fieldAxm%22%3A%22161910229%22%2C%22fieldAxm_Name%22%3A%22%E5%BC%A0%E7%82%80%22%2C%22fieldAxy%22%3A%220518000%22%2C%22fieldAxy_Name%22%3A%22%E9%95%BF%E7%A9%BA%E5%AD%A6%E9%99%A2%22%2C%22fieldAxh%22%3A%22161910229%22%2C%22fieldAlxdh%22%3A%2215862949119%22%2C%22fieldAfdy%22%3A%2270207061%22%2C%22fieldAfdy_Name%22%3A%22%E9%99%B6%E7%84%B6%E9%9B%81%22%2C%22fieldDS%22%3A%22%22%2C%22fieldDS_Name%22%3A%22%22%2C%22fieldASFZHM%22%3A%22321181200012170011%22%2C%22fieldASZXQ%22%3A%222%22%2C%22fieldASZXQ_Name%22%3A%22%E5%B0%86%E5%86%9B%E8%B7%AF%E6%A0%A1%E5%8C%BA%22%2C%22fieldXSLX%22%3A%22%E4%BD%8F%E6%A0%A1%22%2C%22fieldXSLX_Name%22%3A%22%E4%BD%8F%E6%A0%A1%22%2C%22fieldSFYGLS%22%3A%22%22%2C%22fieldTZSFJK%22%3A%22%22%2C%22fieldSKM%22%3A%22%7B%5C%22id%5C%22%3A%5C%220d9c1d86-8bfc-41fb-869f-9c9a25efbefb%5C%22%2C%5C%22name%5C%22%3A%5C%221.jpg%5C%22%2C%5C%22size%5C%22%3A2%2C%5C%22uri%5C%22%3A%5C%22https%3A%2F%2Fehall.nuaa.edu.cn%2Ffile%2F0d9c1d86-8bfc-41fb-869f-9c9a25efbefb%5C%22%2C%5C%22mime%5C%22%3A%5C%22image%2Fjpeg%5C%22%7D%22%2C%22fieldXCM%22%3A%22%7B%5C%22id%5C%22%3A%5C%224381cbb0-fd83-4d4f-abed-33b57c8126d7%5C%22%2C%5C%22name%5C%22%3A%5C%221.jpg%5C%22%2C%5C%22size%5C%22%3A2%2C%5C%22uri%5C%22%3A%5C%22https%3A%2F%2Fehall.nuaa.edu.cn%2Ffile%2F4381cbb0-fd83-4d4f-abed-33b57c8126d7%5C%22%2C%5C%22mime%5C%22%3A%5C%22image%2Fjpeg%5C%22%7D%22%2C%22fieldHSBG%22%3A%22%7B%5C%22id%5C%22%3A%5C%22180502a3-57ae-4a1c-81e9-af367cddc107%5C%22%2C%5C%22name%5C%22%3A%5C%221.jpg%5C%22%2C%5C%22size%5C%22%3A2%2C%5C%22uri%5C%22%3A%5C%22https%3A%2F%2Fehall.nuaa.edu.cn%2Ffile%2F180502a3-57ae-4a1c-81e9-af367cddc107%5C%22%2C%5C%22mime%5C%22%3A%5C%22image%2Fjpeg%5C%22%7D%22%2C%22fieldBLHTS%22%3A%22%22%2C%22fieldCXRQ%22%3A1668009600%2C%22fieldJSSJ%22%3A1668009600%2C%22fieldCXSJFROM%22%3A0%2C%22fieldCXSJTO%22%3A300%2C%22fieldCXSY%22%3A%22.%22%2C%22fieldCXLB%22%3A%221%22%2C%22fieldAcxxc%22%3A%222%22%2C%22fieldAds%22%3A%221%22%2C%22fieldAshengs%22%3A%5B%22%22%5D%2C%22fieldAshengs_Name%22%3A%5B%22%22%5D%2C%22fieldAshis%22%3A%5B%22%22%5D%2C%22fieldAshis_Name%22%3A%5B%22%22%5D%2C%22fieldAshis_Attr%22%3A%5B%22%7B%5C%22_parent%5C%22%3A%5C%22%5C%22%7D%22%5D%2C%22fieldAjtdd%22%3A%5B%22%22%5D%2C%22fieldCN%22%3Atrue%2C%22fieldAhidden%22%3A%22%22%2C%22fieldCyj3%22%3A%22%22%2C%22fieldCshr3%22%3A%22%22%2C%22fieldCshr3_Name%22%3A%22%22%2C%22fieldCshdate3%22%3A%22%22%2C%22fieldFYZSH%22%3A%22%22%2C%22fieldFYZSHR%22%3A%22%22%2C%22fieldFYZSHR_Name%22%3A%22%22%2C%22fieldFYZSHRQ%22%3A%22%22%2C%22fieldCyj4%22%3A%22%22%2C%22fieldCshr4%22%3A%22%22%2C%22fieldCshr4_Name%22%3A%22%22%2C%22fieldCshdate4%22%3A%22%22%2C%22fieldCyj5%22%3A%22%22%2C%22fieldCshr5%22%3A%22%22%2C%22fieldCshr5_Name%22%3A%22%22%2C%22fieldCshsj5%22%3A%22%22%2C%22fieldTOKEN%22%3A%22%22%2C%22fieldCXRQSTR%22%3A%22%22%2C%22fieldCXRQFrom%22%3A1668072325%2C%22fieldFZZD%22%3A%22%22%7D&remark=&rand=498.95878385894457&nextUsers=%7B%222%2C%22%3A%227e012e08-c95e-11e9-9127-0050568a281f%22%7D&stepId=19894858&timestamp=1668072324&boundFields=fieldCXSJTO%2CfieldASZXQ%2CfieldCXRQ%2CfieldAshengs%2CfieldAcxxc%2CfieldAxh%2CfieldFZZD%2CfieldCXRQSTR%2CfieldSKM%2CfieldAxm%2CfieldAlxdh%2CfieldCXRQFrom%2CfieldDS%2CfieldXCM%2CfieldTOKEN%2CfieldXSLX%2CfieldSFYGLS%2CfieldHMDFZ%2CfieldBLHTS%2CfieldAhidden%2CfieldFYZSH%2CfieldJSSJ%2CfieldCXLB%2CfieldSQSJ%2CfieldCshr3%2CfieldTZSFJK%2CfieldASFZHM%2CfieldCN%2CfieldFYZSHRQ%2CfieldCXSJFROM%2CfieldFYZSHR%2CfieldCshdate3%2CfieldXSSF%2CfieldCshsj5%2CfieldAjtdd%2CfieldAxy%2CfieldHSBG%2CfieldCshdate4%2CfieldAfdy%2CfieldCXSY%2CfieldAds%2CfieldCshr4%2CfieldCshr5%2CfieldCyj3%2CfieldCyj5%2CfieldCyj4%2CfieldAshis&csrfToken=qHI2cSc0R855VVVUwz6M4cRpOk8ziTay&lang=zh
'''
item = {
    "stepId"               : r"form/(\d+)/render",
    "fieldAfdy"            : r"fieldAfdy%22%3A%22(.{8})%22",
    "timestamp"            : r"timestamp=(\d+)&",
    "jsessionID"           : r"Cookie:\s(.+)",
    "csrfToken"            : r"csrfToken=(.+)&",
    "leaveSchool_timestamp": r"_VAR_TODAY%22%3A%22(\d+)%22",
    "Studept"              : r"ORGANIZES_Codes%22%3A%22(\d+)%22",
    "ip"                   : r"_VAR_ADDR%22%3A%22(.+\.\d+)%22"
}
subst = {
    "stepId"               : "{0}",
    "fieldAfdy"            : "{1}",
    "timestamp"            : "{2}",
    "jsessionID"           : "JSESSIONID={3}",
    "csrfToken"            : "{4}",
    "leaveSchool_timestamp": "{5}",
    "Studept"              : "{6}",
    "ip"                   : "10.100.109.144"
}
for i in item.keys():
    match = re.findall(item[i], result)
    print(i, match[0])
    result = re.sub(match[0], subst[i], result, 0, re.MULTILINE)
    
if result:
    print (result)