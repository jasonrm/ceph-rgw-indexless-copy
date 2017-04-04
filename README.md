## ceph-rgw-indexless-copy 

Did ceph rgw erase your bucket index?

This will iterate over all rados objects in a pool and copy them via radosgw to a new S3 location

### Requirements

* python3
* ceph + librados + python3 bindings

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
