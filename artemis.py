#!/usr/bin/env python
import os, re, pathlib, sys, datetime
import pandas as pd
import cx_Oracle
import modules.logger
from datetime import datetime
from sqlalchemy import create_engine, text, update
from modules.file_utils import FileUtils
from modules.blob_utils import BlobUtils
from modules.env_utils import EnvUtils
from modules.port_scan_utils import PortScanUtils

if __name__ == '__main__':
    ROOTDIR='adf'
    progname = sys.argv[0]
    log_file = re.sub('\.py', ".log", progname)
    log = modules.logger.get_logger(progname, filename=log_file)
    numargs = len(sys.argv)
    sqlInvServerPort = "1433"
    for argidx in range(1, numargs, 2):
        if sys.argv[argidx] == "-dbEngine":
            dbEngine = sys.argv[argidx + 1]
        if sys.argv[argidx] == "-sqlAssessUser":
            sqlAssessUser = sys.argv[argidx + 1]
        if sys.argv[argidx] == "-sqlAssessPwd":
            sqlAssessPwd = sys.argv[argidx + 1]
        if sys.argv[argidx] == "-sqlAdmin":
            sqlAdmin = sys.argv[argidx + 1]
        if sys.argv[argidx] == "-sqlAdminPwd":
            sqlAdminPwd = sys.argv[argidx + 1]
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
        if sys.argv[argidx] == "-sqlInvSch":
            sqlInvSch = sys.argv[argidx + 1]
        if sys.argv[argidx] == "-sqlInvTbl":
            sqlInvTbl = sys.argv[argidx + 1]
        if sys.argv[argidx] == "-perfStatAuth":
            perfStatAuth = sys.argv[argidx + 1]
        if sys.argv[argidx] == "-perfStatPwd":
            perfStatPwd = sys.argv[argidx + 1]
    if dbEngine == "SQL Server":
        BASEDIR=os.path.join('aaf-query-engine','sql-query-package')
        ENGINE="SQL Server"
    if dbEngine == "Oracle":
        BASEDIR=os.path.join('aaf-query-engine','oracle-query-package')
        ENGINE='Oracle'
    OUTDIR=os.path.join(ROOTDIR,ENGINE)
    query_files = os.path.join(BASEDIR, 'query_files.txt')

    inv_conn_str = r'mssql+pymssql://' + sqlAdmin + ':' + sqlAdminPwd + '@' + sqlInvServer + ':' + sqlInvServerPort + '/' + sqlInvDb
    log.info("Connecting to InventoryDB at host %s database %s port %s " % (sqlInvServer, sqlInvDb, sqlInvServerPort ))
    inv_engine  = create_engine(inv_conn_str)
    if dbEngine == 'SQL Server':
        server_stmt = "select distinct \"Instance Name\", \"Port Number\", \"Host Name\" from \"" + sqlInvSch + "\".\"" + sqlInvTbl + "\" where \"Database Engine\" = \'" + ENGINE + "\' and \"Connectivity\" = 1 and \"Assessment Tool\" = \'AAFQE\'"
    if dbEngine == 'Oracle':
        server_stmt = "select * from \"" + sqlInvSch + "\".\"" + sqlInvTbl + "\" where \"Database Engine\" = \'" + ENGINE + "\' and \"Connectivity\" = 1 and \"Assessment Tool\" = \'AAFQE\'"
    log.info("Running following statement on InventoryDB: %s " % (server_stmt))
    db_servers = pd.read_sql_query(sql=text(server_stmt), con=inv_engine.connect())

    if dbEngine == "SQL Server":
        assess_database = "MASTER"
        db_user = sqlAssessUser
        db_password = sqlAssessPwd
    if dbEngine == "Oracle":
        db_user = oraAssessUser
        db_password = oraAssessPwd

    for index in db_servers.index:
        db_hostname = db_servers['Host Name'][index]
        db_port = str(db_servers['Port Number'][index])
        port_scan = PortScanUtils()
        if not port_scan.check_if_port_open(db_hostname, int(db_port)):
            log.info("Port: %s not open on host: %s" % (db_port, db_hostname))
            try:
                upd_conn = inv_engine.connect()
                upd_result = upd_conn.execute(text('UPDATE \"' + sqlInvTbl + '\" SET \"Connectivity\" = 0 where \"Host Name\" = \'' + db_hostname +"\'"))
                upd_conn.commit()
            except Exception as e:
                log.error("Updating aaf-inventory failed. Statement: %s Error: %s" % (upd_result, e))
            continue
        if dbEngine != 'SQL Server':
            assess_database = db_servers['Database Name'][index]
        log.info("DB Server assessing now: %s" % db_hostname)
        if dbEngine == "SQL Server":
            conn_str = r'mssql+pymssql://' + db_user + ':' + db_password + '@' + db_hostname + ':' + db_port+ '/' + assess_database
        if dbEngine == "Oracle":
            conn_str = r'oracle+cx_oracle://' + db_user  + ':' + db_password +'@' + db_hostname + ':' + db_port + '/' + assess_database
        log.info("Connecting to host %s database %s to do the assessment." % (db_hostname, assess_database))
        try:
            engine = create_engine(conn_str)
        except Exception as e:
            log.error("Error while connecting to host %s database %s: %s" % (db_hostname, assess_database, e))
            try:
                upd_conn = inv_engine.connect()
                upd_result = upd_conn.execute(text('UPDATE \"' + sqlInvTbl + '\" SET \"Connectivity\" = 0 where \"Host Name\" = \'' + db_hostname +"\'"))
                upd_conn.commit()
            except Exception as e:
                log.error("Updating aaf-inventory failed. Statement: %s Error: %s" % (upd_result, e))
            continue
        with open(query_files) as file:
            queries = [line.rstrip() for line in file]
        file.close()
        for query_file in queries:
            now = datetime.utcnow()
            filedatetime = now.strftime("%Y-%m-%d-%H.%M.%S.%f")[:-3]
            file = os.path.join(BASEDIR, query_file)
            f = open(file, 'r')
            sql_stmt = f.read()
            f.close()
            try:
                df = pd.read_sql_query(sql=text(sql_stmt), con=engine.connect())
            except Exception as e:
                log.error("Error while running query on host %s database %s: %s" % (db_hostname, assess_database, e))
                try:
                    upd_conn =inv_engine.connect()
                    upd_result = upd_conn.execute(text('UPDATE \"' + sqlInvTbl + '\" SET \"Connectivity\" = 0 where \"Host Name\" = \'' + db_hostname +"\'"))
                    upd_conn.commit()
                except Exception as e:
                    log.error("Updating aaf-inventory failed. Statement: %s Error: %s" % (upd_result, e))
                continue
            try:
                upd_conn =inv_engine.connect()
                if dbEngine != "SQL Server":
                    upd_result = upd_conn.execute(text("UPDATE \"" + sqlInvTbl + "\" SET \"Assessed\" = 1 where \"Host Name\" = \'" + db_hostname + "\' and \"Database Name\" = \'"  + assess_database + "\'"))
                    upd_conn.commit()
                else:
                    upd_result = upd_conn.execute(text("UPDATE \"" + sqlInvTbl + "\" SET \"Assessed\" = 1 where \"Host Name\" = \'" + db_hostname + "\'"))
                    upd_conn.commit()

            except Exception as e:
                log.error("Updating aaf-inventory failed. Statement: %s Error: %s" % (upd_result, e))

            postfix = '-' + filedatetime + '.csv'
            csv_file = re.sub('\.sql', postfix, query_file)
            container = re.sub('\.sql', '', query_file)
            report_dir = os.path.join(OUTDIR, container)
            if not os.path.exists(report_dir):
                try:
                    os.makedirs(report_dir, exist_ok=True)
                except IOError:
                    sys.exit(1)
            df.insert(0, 'Device Name', db_hostname)
            output_file = os.path.join(report_dir, csv_file)
            df.to_csv(output_file, index=False)
        log.info("Closing connection to host %s database %s." % (db_hostname, assess_database))
        engine.dispose()
    log.info("Assesments done")

    log.info("Uploading results to Azure Storage Account")
    file_utils = FileUtils()
    blob_utils = BlobUtils()
    input_dir=os.path.join(ROOTDIR, ENGINE)
    if os.path.isdir(input_dir):
        containers = os.listdir(input_dir)
        for container_name in containers:
            blob_utils.create_container_if_not_exist(container_name)
            file_dir = os.path.join(input_dir, container_name)
            csv_files = file_utils.find_files('.csv', file_dir)
            for  csv_file in csv_files:
                blob_utils.upload_to_blob(csv_file, container_name)
        log.info("Uploaded csv files to Azure Storage Account done")
    else:
        log.info("No files to upload Azure Storage Account done")
    log.info("Closing connection to  to InventoryDB")
    try:
        inv_engine.dispose()
        log.info("Connection closed to InventoryDB")
    except Exception as e:
        log.error("Failed closing connection to InventoryDB: %s" % e)
    sys.exit(0)
