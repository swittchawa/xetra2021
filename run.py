"""Running the Xetra ETL application"""
import argparse
import logging
import logging.config

import yaml

from xetra.common.s3 import S3BucketConnector
from xetra.transformers.xetra_transformer import XetraETL, XetraSourceConfig, XetraTargetConfig

def main():
    """
        entry point to run the Xetra ETL job
    """
    # Parsing the YAML file
    parser = argparse.ArgumentParser(description='Run the Xetra ETL job.')
    config_path = '/Users/swittchawanwanidchai/xetra_project/xetra2021/configs/xetra_report1_config.yml'
    args = parser.parse_args()
    config = yaml.safe_load(open(config_path))

    # Configure logging
    log_config = config['logging']
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)
    # reading s3 configuration
    s3_config = config['s3']
    # Creating the S3BucketConnector class instances for source and target
    s3_bucket_src = S3BucketConnector(access_key=s3_config['access_key'],
                                        secret_key=s3_config['secret_key'],
                                        endpoint_url=s3_config['src_endpoint_url'],
                                        bucket=s3_config['src_bucket'])
    s3_bucket_trg = S3BucketConnector(access_key=s3_config['access_key'],
                                        secret_key=s3_config['secret_key'],
                                        endpoint_url=s3_config['trg_endpoint_url'],
                                        bucket=s3_config['trg_bucket'])
    # Reading source configuration
    source_config = XetraSourceConfig(**config['source'])
    # Reading target configuration
    target_config = XetraTargetConfig(**config['target'])
    # Reading meta file configuration
    meta_config = config['meta']
    # Creating XetraETL class instance
    logger.info('Xetra ETL job started')
    xetra_etl = XetraETL(s3_bucket_src, s3_bucket_trg,
                            meta_config['meta_key'], source_config, target_config)
    # running ETL job for xetra report
    xetra_etl.etl_report1()
    logger.info('Xetra ETL job finished.')

if __name__ == '__main__':
    main()
