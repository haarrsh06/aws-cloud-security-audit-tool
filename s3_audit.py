import boto3

s3 = boto3.client('s3')


def check_public_buckets():
    buckets = s3.list_buckets()['Buckets']

    print("\n[+] Checking S3 bucket permissions...\n")

    for bucket in buckets:
        bucket_name = bucket['Name']

        try:
            acl = s3.get_bucket_acl(Bucket=bucket_name)

            for grant in acl['Grants']:
                grantee = grant.get('Grantee', {})

                if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AllUsers':
                    print(f"[CRITICAL] Public bucket detected: {bucket_name}")

        except Exception as error:
            print(f"[ERROR] {bucket_name}: {error}")


if __name__ == '__main__':
    check_public_buckets()
