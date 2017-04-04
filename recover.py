import logging
import mimetypes
from argparse import ArgumentParser
from configparser import ConfigParser
from re import compile

from boto3 import Session as BotoSession
from botocore.client import Config
from os import path, getenv
from rados import Rados as CephRados


class Rados:
    ignored_prefixes = ['_shadow', '_multipart']

    def __init__(self, bucket_marker, ceph_conf):
        self.bucket_marker = bucket_marker
        self.cluster = CephRados(conffile=ceph_conf)
        self.cluster.connect()

    def list_objects(self, key_regex):
        filter = compile("{}_(?!({}))({})".format(self.bucket_marker, "|".join(self.ignored_prefixes), args.key_regex))
        with self.cluster.open_ioctx('default.rgw.buckets.data') as ioctx:
            for obj in ioctx.list_objects():
                match = filter.match(obj.key)
                if match is None:
                    continue
                file_path = match.group(2)
                yield file_path


def configured_boto_client(profile):
    credentials = ConfigParser()
    credentials_path = path.join(path.expanduser('~'), '.aws', 'credentials')
    credentials.read(credentials_path)

    config = ConfigParser()
    config_path = path.join(path.expanduser('~'), '.aws', 'config')
    config.read(config_path)

    aws_access_key_id = credentials[profile]['aws_access_key_id']
    aws_secret_access_key = credentials[profile]['aws_secret_access_key']
    try:
        endpoint_url = config['profile {!s}'.format(profile)]['endpoint_url']
    except KeyError:
        endpoint_url = None

    session = BotoSession()
    return session.client(
        service_name='s3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        config=Config(s3={'addressing_style': 'path'})
    )


#
log_level = getenv('LOG_LEVEL', logging.INFO)
logging.basicConfig(level=log_level, format='%(asctime)s %(levelname)-8s %(message)s')
mimetypes.init()

#
parser = ArgumentParser()
parser.add_argument("--source-bucket-marker", required=True, help="Source bucket marker")
parser.add_argument("--source-bucket-name", required=True, help="Source bucket name")
parser.add_argument("--target-bucket-name", required=True, help="Target bucket name")
parser.add_argument("--source-bucket-profile", default="default", help="Profile to use for source bucket")
parser.add_argument("--target-bucket-profile", default="default", help="Profile to use for target bucket")
parser.add_argument("--dry-run", action='store_true', help="Dry Run")
parser.add_argument("--guess-content-type", action='store_true', help="Reset the content type using best guess from key extension")
parser.add_argument("--key-regex", default=".*", help="Only process keys matching regex")
parser.add_argument("--ceph-conf", default="/etc/ceph/ceph.conf", help="Location of ceph.conf file")
args = parser.parse_args()

#
rados = Rados(bucket_marker=args.source_bucket_marker, ceph_conf=args.ceph_conf)
source = configured_boto_client(args.source_bucket_profile)
target = configured_boto_client(args.target_bucket_profile)
dry_run = args.dry_run

logging.info('Source bucket marker: {}'.format(args.source_bucket_marker))
logging.info('Source bucket : {}'.format(args.source_bucket_name))
logging.info('Source profile: {}'.format(args.source_bucket_profile))
logging.info('Target bucket : {}'.format(args.target_bucket_name))
logging.info('Target profile: {}'.format(args.target_bucket_profile))
logging.info('Key regex: {}'.format(args.key_regex))
logging.info('Dry Run: {}'.format(args.dry_run or False))

for key in rados.list_objects(args.key_regex):
    try:
        reference = {
            'Bucket': args.source_bucket_name,
            'Key': key
        }
        extra_args = {
            'ACL': 'private',
            'MetadataDirective': 'REPLACE'
        }
        if args.guess_content_type:
            content_type = mimetypes.guess_type(key)[0] or ""
            logging.info('Guessed content-type "{}" for key "{}"'.format(content_type, key))
            extra_args['ContentType'] = content_type
        if not dry_run:
            logging.info('Copying key "{}"'.format(key))
            target.copy(reference, args.target_bucket_name, key, ExtraArgs=extra_args)
        else:
            logging.info('Would copy key "{}"'.format(key))
    except:
        logging.error('Failed to copy key "{}"'.format(key))
    logging.debug('searching...')
