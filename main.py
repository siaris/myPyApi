from fastapi import FastAPI
import mysql.connector
import json

con = open('db-prima', 'r').read().splitlines()
how = 'local'

mydb = mysql.connector.connect(
  host=con[0] if how == 'public' else con[1],
  user=con[2],
  password=con[3],
  database=con[4],
  autocommit=True
)
mycursor = mydb.cursor(dictionary=True)

app = FastAPI()

@app.get("/")
async def root():
    dtdic = get_erm_result_from_DR('3296831')
    return dtdic





def exec_q(qT):
  mycursor.execute(qT)
  myresult = mycursor.fetchall()
  jD = []
  for x in myresult:
    jD.append(x['json_result'])
  JReturn = '['+','.join(jD)+']'
  return JReturn

def exec_to_result(q):
  mycursor.execute(q)
  return mycursor.fetchall()

def get_erm_result(code,v='',limit=''):
    verQ = ' TRUE ' if v=='' else ' versi = "'+v+'" '
    limQ = '' if limit=='' else ' LIMIT '+limit 
    return exec_q("select json_result from primaprod.mr_result inner join primaprod.mr_form on \
id_form=mr_form.id where kode like '"+code+"' AND "+verQ+limQ)

def get_erm_result_from_RM(rm):
  #dapatkan barisan DR
  rawPKP = exec_to_result("select poli_kunjungan_pasien.attr_tambahan from poli_kunjungan_pasien inner join pendaftaran\
    using (no_reg) where pendaftaran.no_rm = '"+rm+"' and poli_kunjungan_pasien.status_ok = 1\
      and attr_tambahan like '%\"emr\":%'")
  return get_attr_emr(rawPKP)

def get_erm_result_from_NOREG(nr):
  #dapatkan barisan attr
  rawPKP = exec_to_result("select attr_tambahan from poli_kunjungan_pasien where no_reg = '"+nr+"' and status_ok = 1\
     and attr_tambahan like '%\"emr\":%'")
  return get_attr_emr(rawPKP)

def get_erm_result_from_DR(dr):
  rawPKP = exec_to_result("select attr_tambahan from poli_kunjungan_pasien where id = '"+dr+"' and status_ok = 1\
    and attr_tambahan like '%\"emr\":%'")
  return get_attr_emr(rawPKP)

def get_attr_emr(attrs):
  EMRid = []
  for i in attrs:
    attr = json.loads(i['attr_tambahan'])
    for j in attr['emr']:
      EMRid.append(j)
  mycursor.execute('select mr_result.id,json_result,kode,user_created from primaprod.mr_result inner join primaprod.mr_form on \
id_form=mr_form.id where mr_result.id in ("'+'","'.join([str(int) for int in EMRid])+'")')
  return parse_code_to_key(mycursor.fetchall()) 

def parse_code_to_key(dic):
  rDic = {}
  for i in dic:
    jR = json.loads(i['json_result'])
    for k in jR:
      rDic[i['kode']+'.'+str(i['user_created'])+'.'+str(i['id'])+'.'+k] = []
      rDic[i['kode']+'.'+str(i['user_created'])+'.'+str(i['id'])+'.'+k].append(jR[k])
  return rDic