#!/usr/bin/env python
import sys

progname = sys.argv[0]
numargs = len(sys.argv)
for argidx in range(1, numargs, 2): 
    if sys.argv[argidx] == "-dbEngine":
        dbEngine = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlAdmin":
        sqlAdmin = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlAdminPwd":
        sqlAdminPwd = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-oraAssessUser":
        oraAssessUser = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-oraAssessPwd":
        oraAssessPwd = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlReader":
        sqlReader = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlReaderPwd":
        sqlReaderPwd = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlInvDb":
        sqlInvDb = sys.argv[argidx + 1]
    if sys.argv[argidx] == "-sqlInvTbl":
        sqlInvTbl = sys.argv[argidx + 1]

with open('/tmp/mssqltest.txt', 'w') as f:
    f.write("sqlAdmin: %s\n" % sqlAdmin)
    f.write("sqlAdminPwd: %s\n" % sqlAdminPwd)
    f.write("oraAssessUser: %s\n" % oraAssessUser)
    f.write("oraAssessPwd: %s\n" % oraAssessPwd)
    f.write("sqlReader: %s\n" % sqlReader)
    f.write("sqlReaderPwd: %s\n" % sqlReaderPwd)
    f.write("sqlInvDb: %s\n" % sqlInvDb)
    f.write("sqlInvTbl: %s\n" % sqlInvTbl)
f.close()
sys.exit(0)
