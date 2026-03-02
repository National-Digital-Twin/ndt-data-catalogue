<!--
SPDX-License-Identifier: OGL-UK-3.0

This file is unmodified from its original version developed by Acryl Data, Inc.,
and is now included as part of a repository maintained by the National Digital Twin Programme.
All support, maintenance and further development of this code is now the responsibility
of the National Digital Twin Programme.
-->

As a prerequisite, you should [create a DataHub Application](https://docs.microsoft.com/en-us/graph/toolkit/get-started/add-aad-app-registration) within the Azure AD Portal with the permissions
to read your organization's Users and Groups. The following permissions are required, with the `Application` permission type:

- `Group.Read.All`
- `GroupMember.Read.All`
- `User.Read.All`

You can add a permission by navigating to the permissions tab in your DataHub application on the Azure AD portal.

<p align="center">
  <img width="70%"  src="https://raw.githubusercontent.com/datahub-project/static-assets/main/imgs/azure-ad/azure_ad_api_permissions.png"/>
</p>

You can view the necessary endpoints to configure by clicking on the Endpoints button in the Overview tab.

<p align="center">
  <img width="70%"  src="https://raw.githubusercontent.com/datahub-project/static-assets/main/imgs/azure-ad/azure_ad_endpoints.png"/>
</p>
