#encoding=utf-8
NETYPES = ['BTS3900','BTS3900 LTE', 'BTS3900 WCDMA']
HOST = ''

NELIST = []

for NETYPE in NETYPES
    NELIST.extend(GetNELstByType(NETYPE))
end

EXECTIME = StrfTime("%Y%m%d_%H%M%S",LocalTime())
SEPARATOR = '|'

OUPUTFILE = 'C:/@@@/ISSTAR_RESULT/DSP_VSWR' +  '_' + HOST +  '.' + EXECTIME +'.csv'
OUPUTFILE_FAIL_REP = 'C:/@@@/ISSTAR_RESULT/DSP_VSWR_FAIL' +  '_' + HOST +  '.' + EXECTIME +'.txt'

Print("Generating File : " + OUPUTFILE)
f = file(OUPUTFILE, 'w+')
f_fail = file(OUPUTFILE_FAIL_REP, 'w+')

MML_CMD = 'DSP VSWR:;'
TOTAL_NE = len(NELIST)
p_NE = 0
for NE in NELIST
    p_NE += 1
    Print("(%s/%s)-Query %s: "%(p_NE, TOTAL_NE, NE))
    if ConnectNE(NE)
        if SendMML(MML_CMD) == 1
            mml_0 = GetMMLReport(-1)
            p_0=ParseMMLRpt(mml_0)
            RETCODE = GetResultCode(p_0)
            if RETCODE == '0'

                title, data = GetDataFrmMMLRpt(p_0,0)
                reportcount = 0
                for r in data
                    if reportcount == 0
                        f.write('NE_NAME')
                    else
                        f.write(NE)
                    end
                    for v in r
                       f.write(SEPARATOR +v)
                    end
                    f.write('\n')
                    reportcount = reportcount  + 1      
                end
           else
               f_fail.write('%s | Return Error Code %s\n'%(NE, GetResultCause(p_0)))
           end
         else
             f_fail.write('%s | Failed to Send MML \n'%(NE))
         end
     else
        f_fail.write('%s | Can\'t Connect\n'%NE)
     end
end
f.close()  
Print("Done") 