## ceph-rgw-indexless-copy 

Did ceph rgw erase your bucket index?

This will iterate over all rados objects in a pool and copy them via radosgw to a new S3 location

### Requirements

* python3
* ceph + librados + python3 bindings
* [S3 config stored in ~/.aws/credentials and ~/.aws/config](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-config-files)

### Install Dependencies

```
pip install boto3
```

### Usage

```
$ python3 ./recover.py 
usage: recover.py [-h] --source-bucket-marker SOURCE_BUCKET_MARKER
                  --source-bucket-name SOURCE_BUCKET_NAME
                  [--source-bucket-profile SOURCE_BUCKET_PROFILE]
                  --target-bucket-name TARGET_BUCKET_NAME
                  [--target-bucket-profile TARGET_BUCKET_PROFILE]
                  [--ceph-conf CEPH_CONF] [--delete-after-copy] [--dry-run]
                  [--guess-content-type] [--key-regex KEY_REGEX]
                  [--rados-pool-name RADOS_POOL_NAME]
                  [--target-acl TARGET_ACL]

optional arguments:
  -h, --help            show this help message and exit
  --source-bucket-marker SOURCE_BUCKET_MARKER
                        Source bucket marker
  --source-bucket-name SOURCE_BUCKET_NAME
                        Source bucket name
  --source-bucket-profile SOURCE_BUCKET_PROFILE
                        Profile to use for source bucket
  --target-bucket-name TARGET_BUCKET_NAME
                        Target bucket name
  --target-bucket-profile TARGET_BUCKET_PROFILE
                        Profile to use for target bucket
  --ceph-conf CEPH_CONF
                        Location of ceph.conf file
  --delete-after-copy   WARNING: destructive operation, will delete source
                        object after copy
  --dry-run             Dry Run
  --guess-content-type  Reset the content type using best guess from key
                        extension
  --key-regex KEY_REGEX
                        Only process keys matching regex
  --rados-pool-name RADOS_POOL_NAME
                        Source rados pool
  --target-acl TARGET_ACL
                        ACL to assign to target copy
```

```
$ python3 ./recover.py \
    --source-bucket-marker bc9deaa9-458b-4622-a50b-c2242ff3c118.104720.1 \
    --source-bucket-name media \
    --source-bucket-profile plex \
    --target-bucket-name new-media \
    --target-bucket-profile plex \
    --target-acl "private" \
    --guess-content-type \
    --delete-after-copy
```
