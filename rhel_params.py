#!/usr/bin/env python
import sys

progname = sys.argv[0]
numargs = len(sys.argv)
for argidx in range(1, numargs, 2): 
    if sys.argv[argidx] == "-dbEngine":
        dbEngine = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlAssessUser":
        sqlAssessUser = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlAssessPwd":
        sqlAssessPwd = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-oraAssessUser":
        oraAssessUser = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-oraAssessPwd":
        oraAssessPwd = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlInvReader":
        sqlInvReader = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlInvReaderPwd":
        sqlInvReaderPwd = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlInvServer":
        sqlInvServer = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlInvDb":
        sqlInvDb = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlInvTbl":
        sqlInvTbl = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-azSpnID":
        azSpnID = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-azSpnSecret":
        azSpnSecret = sys.argv[argidx + 1]


with open('/tmp/mssqltest.txt', 'w') as f:
    f.write("dbEngine: %s\n" % dbEngine)
    f.write("sqlAssessUser: %s\n" % sqlAssessUser)
    f.write("sqlAssessPwd: %s\n" % sqlAssessPwd)
    f.write("oraAssessUser: %s\n" % oraAssessUser)
    f.write("oraAssessPwd: %s\n" % oraAssessPwd)
    f.write("sqlInvReader: %s\n" % sqlInvReader)
    f.write("sqlInvReaderPwd: %s\n" % sqlInvReaderPwd)
    f.write("sqlInvServer: %s\n" % sqlInvServer)
    f.write("sqlInvDb: %s\n" % sqlInvDb)
    f.write("sqlInvTbl: %s\n" % sqlInvTbl)
    f.write("azSpnID: %s\n" % azSpnID)
    f.write("azSpnSecret: %s\n" % azSpnSecret)
f.close()
sys.exit(0)









#with open('/tmp/mssqltest.txt', 'w') as f:
#    for arg in sys.argv:
#        f.write(arg + " ")
#    f.write("\n")
#f.close()
#sys.exit(0)


