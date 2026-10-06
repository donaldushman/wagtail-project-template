from django.conf import settings
from storages.backends.s3 import S3Storage


class S3BackupStorage(S3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    region_name = settings.AWS_S3_REGION_NAME
    location = settings.DATABASE_BACKUP_LOCATION
    file_overwrite = False
    default_acl = None
    querystring_auth = False
