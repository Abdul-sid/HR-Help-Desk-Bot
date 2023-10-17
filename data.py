from jira import JIRA

jira = JIRA(basic_auth=('<Username>', '<Password>'), options={'server': '<Jira Server Link>'})

# Expand fields to get the required data
metas = jira.createmeta(projectKeys='<Jira Project Key>', expand='projects.issuetypes.fields')

# ---------------------- Print Reported Types -------------------------
RT_values = []
RT_cert_values = metas['projects'][0]['issuetypes'][0]['fields']['customfield_10230']['allowedValues']
RT_valuesDic = []


for i in range(len(RT_cert_values)):
    RT_values.append(RT_cert_values[i]['value'])
   
for index, value in enumerate(RT_values):
    ds = {'title': RT_values[index], 'value': RT_values[index]}
    RT_valuesDic.append(ds)

# ---------------------- Print Request Types ------------------------
ReqT_values = []
ReqT_cert_values = metas['projects'][0]['issuetypes'][0]['fields']['customfield_20801']['allowedValues']
ReqT_valuesDic = []

for i in range(len(ReqT_cert_values)):
    ReqT_values.append(ReqT_cert_values[i]['value'])
   
for index, value in enumerate(ReqT_values):
    ds = {'title': ReqT_values[index], 'value': ReqT_values[index]}
    ReqT_valuesDic.append(ds)

# -------------------Sub Categories of Request Types--------------------
ReqT_values_2 = []
ReqT_values_Dict_2 = []

for i in range(len(ReqT_cert_values)):
    try:
        for q in range(len(ReqT_cert_values[i]['children'])):
            ReqT_values_2.append(ReqT_cert_values[i]['children'][q]['value'].strip())
    except:
            ReqT_values_2.append("NA")

for index, value in enumerate(ReqT_values_2):
    RT = {'title': ReqT_values_2[index], 'value': ReqT_values_2[index]}
    ReqT_values_Dict_2.append(RT)

print("-------------------------------------")
J = []

for i in range(len(ReqT_cert_values)):
    try: 
        J.append(len(ReqT_cert_values[i]['children']))
    except:
        J.append(1)

fin_val = []
a = 0
y = 0
for k in J:

        fin_val.append(ReqT_values_Dict_2[y:k+a])
        y = k + a
        a = k + a

benifit_array = []

for i in range(len(ReqT_cert_values)):
    benifit_array.append(ReqT_cert_values[i]['value'])

Fin_req_types = dict(zip(benifit_array, fin_val))