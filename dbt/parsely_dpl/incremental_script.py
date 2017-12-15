

import datetime
import argparse
import subprocess
import os
import parsely_raw_data.redshift as redshift
import logging
import logging.handlers

log = logging.getLogger("my-logger")

def daterange(d1, d2):
    return (d1 + datetime.timedelta(days=i) for i in range((d2 - d1).days + 1))


def main():
    parser = argparse.ArgumentParser(description='Run the historical back population of Parse.ly DPL data')
    parser.add_argument('--target_table', nargs='?', default=None,
                        help='The target table for temporarily storing incremental data. This will be truncated after each load')
    parser.add_argument('--redshift_host', nargs='?', default=None,
                        help='The Redshift host found in AWS.')
    parser.add_argument('--redshift_user', nargs='?', default=None,
                        help='The Redshift user used to create tables and migrate data from S3 to Redshift')
    parser.add_argument('--redshift_password', nargs='?', default=None,
                        help='The Redshift password for the user')
    parser.add_argument('--redshift_database', nargs='?', default=None,
                        help='The Redshift database')
    parser.add_argument('--redshift_port', nargs='?', default=None,
                        help='The Redshift port')
    parser.add_argument('--aws_access_key_id', nargs='?', default=None,
                        help='The AWS Access key')
    parser.add_argument('--aws_secret_access_key', nargs='?', default=None,
                        help='The AWS Secret Access key')
    parser.add_argument('--keep_extra_data', nargs='?', default='False',
                        help='Keep extra data field, default is Yes.')
    parser.add_argument('--dpl_network', nargs='?', default=None,
                        help='The network name of dpl data in S3')
    parser.add_argument('--start_date', nargs='?', default=None,
                        help='The first day to process data from S3 to Redshift')
    args = parser.parse_args()
    #names = generate_names(letter=args.letter)
    log.info("1. Made it past arg definition")
    now = datetime.datetime.now()
    today = now.date()
    startdate = datetime.datetime.strptime(args.start_date, "%Y%m%d").date()
    log.info("2. Entering for loop")
    for d in daterange(startdate, today):
        log.info("3. For looping")
        prefix = 'events/'+ d.strftime('%Y/%m/%d')
        #print prefix
        #run copy_from_s3
        redshift.copy_from_s3(network=args.dpl_network, s3_prefix=prefix,table_name=args.target_table,host=args.redshift_host,user=args.redshift_user,password=args.redshift_password,database=args.redshift_database,port=args.redshift_port,access_key_id=args.aws_access_key_id,secret_access_key=args.aws_secret_access_key)
        log.info("Past copy from s3")
        #run dbt command
        #./dbt run --models base.*+
        #dbt_main_module.main(model="base.*+")
        #os.chdir("/dbt/parsely_dpl" )
        dpl_wd = os.path.join(os.getcwd(), 'parsely_raw_data/dbt/parsely_dpl/')
        #print dpl_wd
        subprocess.call(dpl_wd + "run_parsely_dpl.sh", shell=True, cwd=dpl_wd)
        log.info("Past call dbt")

if __name__ == "__main__":
    main()