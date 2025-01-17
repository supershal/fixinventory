from __future__ import annotations

import logging
from datetime import datetime
from typing import ClassVar, Dict, Optional, List, Type

from attr import define, field

from fix_plugin_azure.azure_client import AzureResourceSpec
from fix_plugin_azure.resource.base import (
    MicrosoftResource,
    AzureSystemData,
    AzureSku,
    AzureIdentity,
    GraphBuilder,
)
from fix_plugin_azure.resource.monitor import AzureMonitorDiagnosticSettings
from fixlib.baseresources import ModelReference
from fixlib.json_bender import Bender, S, ForallBend, Bend
from fixlib.types import Json

log = logging.getLogger("fix.plugins.azure")
service_name = "azure_keyvault"


@define(eq=False, slots=False)
class AzureMHSMGeoReplicatedRegion:
    kind: ClassVar[str] = "azure_mhsm_geo_replicated_region"
    mapping: ClassVar[Dict[str, Bender]] = {
        "is_primary": S("isPrimary"),
        "name": S("name"),
        "provisioning_state": S("provisioningState"),
    }
    is_primary: Optional[bool] = field(default=None, metadata={'description': 'A boolean value that indicates whether the region is the primary region or a secondary region.'})  # fmt: skip
    name: Optional[str] = field(default=None, metadata={"description": "Name of the geo replicated region."})
    provisioning_state: Optional[str] = field(default=None, metadata={'description': 'The current provisioning state.'})  # fmt: skip


@define(eq=False, slots=False)
class AzureMHSMPrivateLinkServiceConnectionState:
    kind: ClassVar[str] = "azure_mhsm_private_link_service_connection_state"
    mapping: ClassVar[Dict[str, Bender]] = {
        "actions_required": S("actionsRequired"),
        "description": S("description"),
        "status": S("status"),
    }
    actions_required: Optional[str] = field(default=None, metadata={'description': 'A message indicating if changes on the service provider require any updates on the consumer.'})  # fmt: skip
    description: Optional[str] = field(default=None, metadata={"description": "The reason for approval or rejection."})
    status: Optional[str] = field(default=None, metadata={"description": "The private endpoint connection status."})


@define(eq=False, slots=False)
class AzureMHSMPrivateEndpointConnectionItem:
    kind: ClassVar[str] = "azure_mhsm_private_endpoint_connection_item"
    mapping: ClassVar[Dict[str, Bender]] = {
        "etag": S("etag"),
        "id": S("id"),
        "private_endpoint": S("properties", "privateEndpoint", "id"),
        "private_link_service_connection_state": S("properties", "privateLinkServiceConnectionState")
        >> Bend(AzureMHSMPrivateLinkServiceConnectionState.mapping),
        "provisioning_state": S("properties", "provisioningState"),
    }
    etag: Optional[str] = field(default=None, metadata={'description': 'Modified whenever there is a change in the state of private endpoint connection.'})  # fmt: skip
    id: Optional[str] = field(default=None, metadata={"description": "Id of private endpoint connection."})
    private_endpoint: Optional[str] = field(default=None, metadata={'description': 'Private endpoint object properties.'})  # fmt: skip
    private_link_service_connection_state: Optional[AzureMHSMPrivateLinkServiceConnectionState] = field(default=None, metadata={'description': 'An object that represents the approval state of the private link connection.'})  # fmt: skip
    provisioning_state: Optional[str] = field(default=None, metadata={'description': 'The current provisioning state.'})  # fmt: skip


@define(eq=False, slots=False)
class AzureManagedHSMSecurityDomainProperties:
    kind: ClassVar[str] = "azure_managed_hsm_security_domain_properties"
    mapping: ClassVar[Dict[str, Bender]] = {
        "activation_status": S("activationStatus"),
        "activation_status_message": S("activationStatusMessage"),
    }
    activation_status: Optional[str] = field(default=None, metadata={"description": "Activation Status"})
    activation_status_message: Optional[str] = field(default=None, metadata={'description': 'Activation Status Message.'})  # fmt: skip


@define(eq=False, slots=False)
class AzureKeyVaultPermissions:
    kind: ClassVar[str] = "azure_key_vault_permissions"
    mapping: ClassVar[Dict[str, Bender]] = {
        "certificates": S("certificates"),
        "keys": S("keys"),
        "secrets": S("secrets"),
        "storage": S("storage"),
    }
    certificates: Optional[List[str]] = field(default=None, metadata={"description": "Permissions to certificates"})
    keys: Optional[List[str]] = field(default=None, metadata={"description": "Permissions to keys"})
    secrets: Optional[List[str]] = field(default=None, metadata={"description": "Permissions to secrets"})
    storage: Optional[List[str]] = field(default=None, metadata={"description": "Permissions to storage accounts"})


@define(eq=False, slots=False)
class AzureAccessKeyVaultPolicyEntry:
    kind: ClassVar[str] = "azure_access_key_vault_policy_entry"
    mapping: ClassVar[Dict[str, Bender]] = {
        "application_id": S("applicationId"),
        "object_id": S("objectId"),
        "permissions": S("permissions") >> Bend(AzureKeyVaultPermissions.mapping),
        "tenant_id": S("tenantId"),
    }
    application_id: Optional[str] = field(default=None, metadata={'description': ' Application ID of the client making request on behalf of a principal'})  # fmt: skip
    object_id: Optional[str] = field(default=None, metadata={'description': 'The object ID of a user, service principal or security group in the Azure Active Directory tenant for the vault. The object ID must be unique for the list of access policies.'})  # fmt: skip
    permissions: Optional[AzureKeyVaultPermissions] = field(default=None, metadata={'description': 'Permissions the identity has for keys, secrets, certificates and storage.'})  # fmt: skip
    tenant_id: Optional[str] = field(default=None, metadata={'description': 'The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault.'})  # fmt: skip


@define(eq=False, slots=False)
class AzureKeyVaultVirtualNetworkRule:
    kind: ClassVar[str] = "azure_key_vault_virtual_network_rule"
    mapping: ClassVar[Dict[str, Bender]] = {
        "id": S("id"),
        "ignore_missing_vnet_service_endpoint": S("ignoreMissingVnetServiceEndpoint"),
    }
    id: Optional[str] = field(default=None, metadata={'description': 'Full resource id of a vnet subnet, such as /subscriptions/subid/resourceGroups/rg1/providers/Microsoft.Network/virtualNetworks/test-vnet/subnets/subnet1 .'})  # fmt: skip
    ignore_missing_vnet_service_endpoint: Optional[bool] = field(default=None, metadata={'description': 'Property to specify whether NRP will ignore the check if parent subnet has serviceEndpoints configured.'})  # fmt: skip


@define(eq=False, slots=False)
class AzureKeyVaultNetworkRuleSet:
    kind: ClassVar[str] = "azure_key_vault_network_rule_set"
    mapping: ClassVar[Dict[str, Bender]] = {
        "bypass": S("bypass"),
        "default_action": S("defaultAction"),
        "ip_rules": S("ipRules", default=[]) >> ForallBend(S("value")),
        "virtual_network_rules": S("virtualNetworkRules") >> ForallBend(AzureKeyVaultVirtualNetworkRule.mapping),
    }
    bypass: Optional[str] = field(default=None, metadata={'description': 'Tells what traffic can bypass network rules. This can be AzureServices or None . If not specified the default is AzureServices .'})  # fmt: skip
    default_action: Optional[str] = field(default=None, metadata={'description': 'The default action when no rule from ipRules and from virtualNetworkRules match. This is only used after the bypass property has been evaluated.'})  # fmt: skip
    ip_rules: Optional[List[str]] = field(default=None, metadata={"description": "The list of IP address rules."})
    virtual_network_rules: Optional[List[AzureKeyVaultVirtualNetworkRule]] = field(default=None, metadata={'description': 'The list of virtual network rules.'})  # fmt: skip


@define(eq=False, slots=False)
class AzureKeyVaultPrivateLinkServiceConnectionState:
    kind: ClassVar[str] = "azure_key_vault_private_link_service_connection_state"
    mapping: ClassVar[Dict[str, Bender]] = {
        "actions_required": S("actionsRequired"),
        "description": S("description"),
        "status": S("status"),
    }
    actions_required: Optional[str] = field(default=None, metadata={'description': 'A message indicating if changes on the service provider require any updates on the consumer.'})  # fmt: skip
    description: Optional[str] = field(default=None, metadata={"description": "The reason for approval or rejection."})
    status: Optional[str] = field(default=None, metadata={"description": "The private endpoint connection status."})


@define(eq=False, slots=False)
class AzureKeyVaultPrivateEndpointConnectionItem:
    kind: ClassVar[str] = "azure_key_vault_private_endpoint_connection_item"
    mapping: ClassVar[Dict[str, Bender]] = {
        "etag": S("etag"),
        "id": S("id"),
        "private_endpoint": S("properties", "privateEndpoint", "id"),
        "private_link_service_connection_state": S("properties", "privateLinkServiceConnectionState")
        >> Bend(AzureKeyVaultPrivateLinkServiceConnectionState.mapping),
        "provisioning_state": S("properties", "provisioningState"),
    }
    etag: Optional[str] = field(default=None, metadata={'description': 'Modified whenever there is a change in the state of private endpoint connection.'})  # fmt: skip
    id: Optional[str] = field(default=None, metadata={"description": "Id of private endpoint connection."})
    private_endpoint: Optional[str] = field(default=None, metadata={'description': 'Private endpoint object properties.'})  # fmt: skip
    private_link_service_connection_state: Optional[AzureKeyVaultPrivateLinkServiceConnectionState] = field(default=None, metadata={'description': 'An object that represents the approval state of the private link connection.'})  # fmt: skip
    provisioning_state: Optional[str] = field(default=None, metadata={'description': 'The current provisioning state.'})  # fmt: skip


@define(eq=False, slots=False)
class AzureKeyAttributes:
    kind: ClassVar[str] = "azure_key_attributes"
    mapping: ClassVar[Dict[str, Bender]] = {
        "created": S("created"),
        "enabled": S("enabled"),
        "exp": S("exp"),
        "exportable": S("exportable"),
        "nbf": S("nbf"),
        "recovery_level": S("recoveryLevel"),
        "updated": S("updated"),
    }
    created: Optional[int] = field(default=None, metadata={'description': 'Creation time in seconds since 1970-01-01T00:00:00Z.'})  # fmt: skip
    enabled: Optional[bool] = field(default=None, metadata={'description': 'Determines whether or not the object is enabled.'})  # fmt: skip
    exp: Optional[int] = field(default=None, metadata={'description': 'Expiry date in seconds since 1970-01-01T00:00:00Z.'})  # fmt: skip
    exportable: Optional[bool] = field(default=None, metadata={'description': 'Indicates if the private key can be exported.'})  # fmt: skip
    nbf: Optional[int] = field(default=None, metadata={'description': 'Not before date in seconds since 1970-01-01T00:00:00Z.'})  # fmt: skip
    recovery_level: Optional[str] = field(default=None, metadata={'description': 'The deletion recovery level currently in effect for the object. If it contains Purgeable , then the object can be permanently deleted by a privileged user; otherwise, only the system can purge the object at the end of the retention interval.'})  # fmt: skip
    updated: Optional[int] = field(default=None, metadata={'description': 'Last updated time in seconds since 1970-01-01T00:00:00Z.'})  # fmt: skip


@define(eq=False, slots=False)
class AzureKeyRotationPolicyAttributes:
    kind: ClassVar[str] = "azure_key_rotation_policy_attributes"
    mapping: ClassVar[Dict[str, Bender]] = {
        "created": S("created"),
        "expiry_time": S("expiryTime"),
        "updated": S("updated"),
    }
    created: Optional[int] = field(default=None, metadata={'description': 'Creation time in seconds since 1970-01-01T00:00:00Z.'})  # fmt: skip
    expiry_time: Optional[str] = field(default=None, metadata={'description': 'The expiration time for the new key version. It should be in ISO8601 format. Eg: P90D , P1Y .'})  # fmt: skip
    updated: Optional[int] = field(default=None, metadata={'description': 'Last updated time in seconds since 1970-01-01T00:00:00Z.'})  # fmt: skip


@define(eq=False, slots=False)
class AzureKeyVaultTrigger:
    kind: ClassVar[str] = "azure_key_vault_trigger"
    mapping: ClassVar[Dict[str, Bender]] = {
        "time_after_create": S("timeAfterCreate"),
        "time_before_expiry": S("timeBeforeExpiry"),
    }
    time_after_create: Optional[str] = field(default=None, metadata={'description': 'The time duration after key creation to rotate the key. It only applies to rotate. It will be in ISO 8601 duration format. Eg: P90D , P1Y .'})  # fmt: skip
    time_before_expiry: Optional[str] = field(default=None, metadata={'description': 'The time duration before key expiring to rotate or notify. It will be in ISO 8601 duration format. Eg: P90D , P1Y .'})  # fmt: skip


@define(eq=False, slots=False)
class AzureKeyVaultLifetimeAction:
    kind: ClassVar[str] = "azure_key_vault_lifetime_action"
    mapping: ClassVar[Dict[str, Bender]] = {
        "action": S("action", "type"),
        "trigger": S("trigger") >> Bend(AzureKeyVaultTrigger.mapping),
    }
    action: Optional[str] = field(default=None, metadata={"description": ""})
    trigger: Optional[AzureKeyVaultTrigger] = field(default=None, metadata={"description": ""})


@define(eq=False, slots=False)
class AzureKeyVaultRotationPolicy:
    kind: ClassVar[str] = "azure_key_vault_rotation_policy"
    mapping: ClassVar[Dict[str, Bender]] = {
        "attributes": S("attributes") >> Bend(AzureKeyRotationPolicyAttributes.mapping),
        "lifetime_actions": S("lifetimeActions") >> ForallBend(AzureKeyVaultLifetimeAction.mapping),
    }
    attributes: Optional[AzureKeyRotationPolicyAttributes] = field(default=None, metadata={"description": ""})
    lifetime_actions: Optional[List[AzureKeyVaultLifetimeAction]] = field(default=None, metadata={'description': 'The lifetimeActions for key rotation action.'})  # fmt: skip


@define(eq=False, slots=False)
class AzureKeyReleasePolicy:
    kind: ClassVar[str] = "azure_key_release_policy"
    mapping: ClassVar[Dict[str, Bender]] = {"content_type": S("contentType"), "data": S("data")}
    content_type: Optional[str] = field(default=None, metadata={'description': 'Content type and version of key release policy'})  # fmt: skip
    data: Optional[str] = field(default=None, metadata={'description': 'Blob encoding the policy rules under which the key can be released.'})  # fmt: skip


@define(eq=False, slots=False)
class AzureManagedHsm(MicrosoftResource):
    kind: ClassVar[str] = "azure_managed_hsm"
    api_spec: ClassVar[AzureResourceSpec] = AzureResourceSpec(
        service="keyvault",
        version="2023-07-01",
        path="/subscriptions/{subscriptionId}/providers/Microsoft.KeyVault/managedHSMs",
        path_parameters=["subscriptionId"],
        query_parameters=["api-version"],
        access_path="value",
        expect_array=True,
    )
    mapping: ClassVar[Dict[str, Bender]] = {
        "id": S("id"),
        "identity": S("identity") >> Bend(AzureIdentity.mapping),
        "location": S("location"),
        "name": S("name"),
        "hsm_sku": S("sku") >> Bend(AzureSku.mapping),
        "system_data": S("systemData") >> Bend(AzureSystemData.mapping),
        "type": S("type"),
        "tags": S("tags", default={}),
        "create_mode": S("properties", "createMode"),
        "enable_purge_protection": S("properties", "enablePurgeProtection"),
        "enable_soft_delete": S("properties", "enableSoftDelete"),
        "hsm_uri": S("properties", "hsmUri"),
        "initial_admin_object_ids": S("properties", "initialAdminObjectIds"),
        "network_acl_rules": S("properties", "networkAcls") >> Bend(AzureKeyVaultNetworkRuleSet.mapping),
        "hsm_private_endpoint_connections": S("properties", "privateEndpointConnections")
        >> ForallBend(AzureMHSMPrivateEndpointConnectionItem.mapping),
        "provisioning_state": S("properties", "provisioningState"),
        "public_network_access": S("properties", "publicNetworkAccess"),
        "regions": S("properties", "regions") >> ForallBend(AzureMHSMGeoReplicatedRegion.mapping),
        "scheduled_purge_date": S("properties", "scheduledPurgeDate"),
        "security_domain_properties": S("properties", "securityDomainProperties")
        >> Bend(AzureManagedHSMSecurityDomainProperties.mapping),
        "soft_delete_retention_in_days": S("properties", "softDeleteRetentionInDays"),
        "status_message": S("properties", "statusMessage"),
        "tenant_id": S("properties", "tenantId"),
    }
    identity: Optional[AzureIdentity] = field(default=None, metadata={'description': 'Managed service identity (system assigned and/or user assigned identities)'})  # fmt: skip
    location: Optional[str] = field(default=None, metadata={'description': 'The supported Azure location where the managed HSM Pool should be created.'})  # fmt: skip
    hsm_sku: Optional[AzureSku] = field(default=None, metadata={"description": "SKU details"})
    system_data: Optional[AzureSystemData] = field(default=None, metadata={'description': 'Metadata pertaining to creation and last modification of the key vault resource.'})  # fmt: skip
    type: Optional[str] = field(default=None, metadata={"description": "The resource type of the managed HSM Pool."})
    create_mode: Optional[str] = field(default=None, metadata={'description': 'The create mode to indicate whether the resource is being created or is being recovered from a deleted resource.'})  # fmt: skip
    enable_purge_protection: Optional[bool] = field(default=None, metadata={'description': 'Property specifying whether protection against purge is enabled for this managed HSM pool. Setting this property to true activates protection against purge for this managed HSM pool and its content - only the Managed HSM service may initiate a hard, irrecoverable deletion. Enabling this functionality is irreversible.'})  # fmt: skip
    enable_soft_delete: Optional[bool] = field(default=None, metadata={'description': 'Property to specify whether the soft delete functionality is enabled for this managed HSM pool. Soft delete is enabled by default for all managed HSMs and is immutable.'})  # fmt: skip
    hsm_uri: Optional[str] = field(default=None, metadata={'description': 'The URI of the managed hsm pool for performing operations on keys.'})  # fmt: skip
    initial_admin_object_ids: Optional[List[str]] = field(default=None, metadata={'description': 'Array of initial administrators object ids for this managed hsm pool.'})  # fmt: skip
    network_acl_rules: Optional[AzureKeyVaultNetworkRuleSet] = field(default=None, metadata={'description': 'A set of rules governing the network accessibility of a managed hsm pool.'})  # fmt: skip
    hsm_private_endpoint_connections: Optional[List[AzureMHSMPrivateEndpointConnectionItem]] = field(default=None, metadata={'description': 'List of private endpoint connections associated with the managed hsm pool.'})  # fmt: skip
    public_network_access: Optional[str] = field(default=None, metadata={'description': 'Control permission to the managed HSM from public networks.'})  # fmt: skip
    regions: Optional[List[AzureMHSMGeoReplicatedRegion]] = field(default=None, metadata={'description': 'List of all regions associated with the managed hsm pool.'})  # fmt: skip
    scheduled_purge_date: Optional[datetime] = field(default=None, metadata={'description': 'The scheduled purge date in UTC.'})  # fmt: skip
    security_domain_properties: Optional[AzureManagedHSMSecurityDomainProperties] = field(default=None, metadata={'description': 'The security domain properties of the managed hsm.'})  # fmt: skip
    soft_delete_retention_in_days: Optional[int] = field(default=None, metadata={'description': 'Soft deleted data retention days. When you delete an HSM or a key, it will remain recoverable for the configured retention period or for a default period of 90 days. It accepts values between 7 and 90.'})  # fmt: skip
    status_message: Optional[str] = field(default=None, metadata={"description": "Resource Status Message."})
    tenant_id: Optional[str] = field(default=None, metadata={'description': 'The Azure Active Directory tenant ID that should be used for authenticating requests to the managed HSM pool.'})  # fmt: skip


@define(eq=False, slots=False)
class AzureKey(MicrosoftResource):
    kind: ClassVar[str] = "azure_key"
    # collected via AzureKeyVault
    mapping: ClassVar[Dict[str, Bender]] = {
        "id": S("id"),
        "tags": S("tags", default={}),
        "name": S("name"),
        "attributes": S("properties", "attributes") >> Bend(AzureKeyAttributes.mapping),
        "curve_name": S("properties", "curveName"),
        "key_ops": S("properties", "keyOps"),
        "key_size": S("properties", "keySize"),
        "key_uri": S("properties", "keyUri"),
        "key_uri_with_version": S("properties", "keyUriWithVersion"),
        "kty": S("properties", "kty"),
        "release_policy": S("properties", "release_policy") >> Bend(AzureKeyReleasePolicy.mapping),
        "rotation_policy": S("properties", "rotationPolicy") >> Bend(AzureKeyVaultRotationPolicy.mapping),
    }
    attributes: Optional[AzureKeyAttributes] = field(default=None, metadata={'description': 'The object attributes managed by the Azure Key Vault service.'})  # fmt: skip
    curve_name: Optional[str] = field(default=None, metadata={'description': 'The elliptic curve name. For valid values, see JsonWebKeyCurveName.'})  # fmt: skip
    key_ops: Optional[List[str]] = field(default=None, metadata={"description": ""})
    key_size: Optional[int] = field(default=None, metadata={'description': 'The key size in bits. For example: 2048, 3072, or 4096 for RSA.'})  # fmt: skip
    key_uri: Optional[str] = field(default=None, metadata={'description': 'The URI to retrieve the current version of the key.'})  # fmt: skip
    key_uri_with_version: Optional[str] = field(default=None, metadata={'description': 'The URI to retrieve the specific version of the key.'})  # fmt: skip
    kty: Optional[str] = field(default=None, metadata={'description': 'The type of the key. For valid values, see JsonWebKeyType.'})  # fmt: skip
    release_policy: Optional[AzureKeyReleasePolicy] = field(default=None, metadata={"description": ""})
    rotation_policy: Optional[AzureKeyVaultRotationPolicy] = field(default=None, metadata={"description": ""})


@define(eq=False, slots=False)
class AzureKeyVault(MicrosoftResource):
    kind: ClassVar[str] = "azure_key_vault"
    api_spec: ClassVar[AzureResourceSpec] = AzureResourceSpec(
        service="keyvault",
        version="2023-07-01",
        path="/subscriptions/{subscriptionId}/providers/Microsoft.KeyVault/vaults",
        path_parameters=["subscriptionId"],
        query_parameters=["api-version"],
        access_path="value",
        expect_array=True,
    )
    reference_kinds: ClassVar[ModelReference] = {
        "successors": {"default": [AzureKey.kind, AzureMonitorDiagnosticSettings.kind]},
    }
    mapping: ClassVar[Dict[str, Bender]] = {
        "id": S("id"),
        "tags": S("tags", default={}),
        "name": S("name"),
        "ctime": S("systemData", "createdAt"),
        "mtime": S("systemData", "lastModifiedAt"),
        "access_policies": S("properties", "accessPolicies") >> ForallBend(AzureAccessKeyVaultPolicyEntry.mapping),
        "create_mode": S("properties", "createMode"),
        "enable_purge_protection": S("properties", "enablePurgeProtection"),
        "enable_rbac_authorization": S("properties", "enableRbacAuthorization"),
        "enable_soft_delete": S("properties", "enableSoftDelete"),
        "enabled_for_deployment": S("properties", "enabledForDeployment"),
        "enabled_for_disk_encryption": S("properties", "enabledForDiskEncryption"),
        "enabled_for_template_deployment": S("properties", "enabledForTemplateDeployment"),
        "hsm_pool_resource_id": S("properties", "hsmPoolResourceId"),
        "network_acl_rules": S("properties", "networkAcls") >> Bend(AzureKeyVaultNetworkRuleSet.mapping),
        "private_endpoint_connections": S("properties", "privateEndpointConnections")
        >> ForallBend(AzureKeyVaultPrivateEndpointConnectionItem.mapping),
        "provisioning_state": S("properties", "provisioningState"),
        "public_network_access": S("properties", "publicNetworkAccess"),
        "vault_sku": S("properties", "sku") >> Bend(AzureSku.mapping),
        "soft_delete_retention_in_days": S("properties", "softDeleteRetentionInDays"),
        "system_data": S("systemData") >> Bend(AzureSystemData.mapping),
        "tenant_id": S("properties", "tenantId"),
        "vault_uri": S("properties", "vaultUri"),
    }
    access_policies: Optional[List[AzureAccessKeyVaultPolicyEntry]] = field(default=None, metadata={'description': 'An array of 0 to 1024 identities that have access to the key vault. All identities in the array must use the same tenant ID as the key vault s tenant ID. When `createMode` is set to `recover`, access policies are not required. Otherwise, access policies are required.'})  # fmt: skip
    create_mode: Optional[str] = field(default=None, metadata={'description': 'The vault s create mode to indicate whether the vault need to be recovered or not.'})  # fmt: skip
    enable_purge_protection: Optional[bool] = field(default=None, metadata={'description': 'Property specifying whether protection against purge is enabled for this vault. Setting this property to true activates protection against purge for this vault and its content - only the Key Vault service may initiate a hard, irrecoverable deletion. The setting is effective only if soft delete is also enabled. Enabling this functionality is irreversible - that is, the property does not accept false as its value.'})  # fmt: skip
    enable_rbac_authorization: Optional[bool] = field(default=None, metadata={'description': 'Property that controls how data actions are authorized. When true, the key vault will use Role Based Access Control (RBAC) for authorization of data actions, and the access policies specified in vault properties will be ignored. When false, the key vault will use the access policies specified in vault properties, and any policy stored on Azure Resource Manager will be ignored. If null or not specified, the vault is created with the default value of false. Note that management actions are always authorized with RBAC.'})  # fmt: skip
    enable_soft_delete: Optional[bool] = field(default=None, metadata={'description': 'Property to specify whether the soft delete functionality is enabled for this key vault. If it s not set to any value(true or false) when creating new key vault, it will be set to true by default. Once set to true, it cannot be reverted to false.'})  # fmt: skip
    enabled_for_deployment: Optional[bool] = field(default=None, metadata={'description': 'Property to specify whether Azure Virtual Machines are permitted to retrieve certificates stored as secrets from the key vault.'})  # fmt: skip
    enabled_for_disk_encryption: Optional[bool] = field(default=None, metadata={'description': 'Property to specify whether Azure Disk Encryption is permitted to retrieve secrets from the vault and unwrap keys.'})  # fmt: skip
    enabled_for_template_deployment: Optional[bool] = field(default=None, metadata={'description': 'Property to specify whether Azure Resource Manager is permitted to retrieve secrets from the key vault.'})  # fmt: skip
    hsm_pool_resource_id: Optional[str] = field(default=None, metadata={"description": "The resource id of HSM Pool."})
    network_acl_rules: Optional[AzureKeyVaultNetworkRuleSet] = field(default=None, metadata={'description': 'A set of rules governing the network accessibility of a vault.'})  # fmt: skip
    vault_private_endpoint_connections: Optional[List[AzureKeyVaultPrivateEndpointConnectionItem]] = field(default=None, metadata={'description': 'List of private endpoint connections associated with the key vault.'})  # fmt: skip
    public_network_access: Optional[str] = field(default=None, metadata={'description': 'Property to specify whether the vault will accept traffic from public internet. If set to disabled all traffic except private endpoint traffic and that that originates from trusted services will be blocked. This will override the set firewall rules, meaning that even if the firewall rules are present we will not honor the rules.'})  # fmt: skip
    vault_sku: Optional[AzureSku] = field(default=None, metadata={"description": "SKU details"})
    soft_delete_retention_in_days: Optional[int] = field(default=None, metadata={'description': 'softDelete data retention days. It accepts >=7 and <=90.'})  # fmt: skip
    system_data: Optional[AzureSystemData] = field(default=None, metadata={'description': 'Metadata pertaining to creation and last modification of the key vault resource.'})  # fmt: skip
    tenant_id: Optional[str] = field(default=None, metadata={'description': 'The Azure Active Directory tenant ID that should be used for authenticating requests to the key vault.'})  # fmt: skip
    vault_uri: Optional[str] = field(default=None, metadata={'description': 'The URI of the vault for performing operations on keys and secrets.'})  # fmt: skip

    def post_process(self, graph_builder: GraphBuilder, source: Json) -> None:
        def collect_keys() -> None:
            for key_json in graph_builder.client.list(
                AzureResourceSpec(
                    service="keyvault",
                    version="2023-07-01",
                    path=f"{self.id}/keys",
                    query_parameters=["api-version"],
                    access_path="value",
                    expect_array=True,
                )
            ):
                if key := AzureKey.from_api(key_json, graph_builder):
                    graph_builder.add_node(key)
                    graph_builder.add_edge(self, node=key)

        graph_builder.submit_work(service_name, collect_keys)
        AzureMonitorDiagnosticSettings.fetch_diagnostics(graph_builder, self)


resources: List[Type[MicrosoftResource]] = [
    AzureManagedHsm,
    AzureKeyVault,
    AzureKey,
]
