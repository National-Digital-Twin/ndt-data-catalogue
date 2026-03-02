<!--
SPDX-License-Identifier: OGL-UK-3.0

This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
-->

### Prerequisites

In order to execute this source the user credentials needs the following privileges

- `grant select on DATABASE.* to 'USERNAME'@'%'`
- `grant show view on DATABASE.* to 'USERNAME'@'%'`

`select` is required to see the table structure as well as for profiling.

### AWS RDS IAM Authentication

For AWS RDS MySQL instances, you can use IAM authentication instead of traditional username/password authentication.

**Setup:**

Follow the [AWS RDS IAM Database Authentication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html) documentation to:

- Enable IAM database authentication on your RDS instance
- Create database users that use IAM authentication
- Configure IAM policies with `rds-db:connect` permissions

**Configuration:**

Set `auth_mode: "AWS_IAM"` in your recipe and optionally configure `aws_config` for AWS credentials and region (see example below). If `aws_config` is not specified, boto3 will automatically use the default credential chain from environment variables, AWS config files, or IAM role metadata.
