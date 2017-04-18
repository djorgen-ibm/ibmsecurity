import logging
import ibmsecurity.utilities.tools
import ibmsecurity.isam.base.network.interfaces

logger = logging.getLogger(__name__)


def add(isamAppliance, label, vlanId, name='', enabled=False, comment='', overrideSubnetChecking=False, bondedTo='',
        bondingMode=None, check_mode=False, force=False):
    """
    Creating a (VLAN) interface
    """
    if force is True or ibmsecurity.isam.base.network.interfaces._get_interface(isamAppliance, label, vlanId) is None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_post("Creating a (VLAN) interface", "/net/ifaces/",
                                             {
                                                 'name': name,
                                                 'label': label,
                                                 'comment': comment,
                                                 'enabled': enabled,
                                                 'vlanId': vlanId,
                                                 'bondedTo': bondedTo,
                                                 'bondingMode': bondingMode,
                                                 'ipv4': {
                                                     'dhcp': {
                                                         'enabled': False,
                                                         'allowManagement': False,
                                                         'providesDefaultRoute': False,
                                                         'routeMetric': None
                                                     },
                                                     'overrideSubnetChecking': overrideSubnetChecking,
                                                     'addresses': []
                                                 },
                                                 'ipv6': {
                                                     'dhcp': {
                                                         'enabled': False,
                                                         'allowManagement': False
                                                     },
                                                     'addresses': []
                                                 }
                                             })

    return isamAppliance.create_return_object()


def delete(isamAppliance, label, vlanId, check_mode=False, force=False):
    """
    Deleting a (VLAN) interface

    NOTE: vlanId needs to be provided, cannot delete default interface with Null vlanId
    """
    ret_obj = None
    if force is False:
        ret_obj = ibmsecurity.isam.base.network.interfaces._get_interface(isamAppliance, label, vlanId)

    if force is True or ret_obj is not None:
        if check_mode is True:
            return isamAppliance.create_return_object(changed=True)
        else:
            return isamAppliance.invoke_delete("Deleting a (VLAN) interface", "/net/ifaces/{0}".format(ret_obj['uuid']))

    return isamAppliance.create_return_object()


def update(isamAppliance, name, comment, label, enabled, vlanId=None, bondedTo='',
           bondingMode=None, check_mode=False, force=False):
    """
    Update existing (VLAN) interface
    """
    update_needed = False
    json_data = {}
    if isinstance(enabled, basestring):
        if enabled.lower() == 'true':
            enabled = True
        else:
            enabled = False
    if force is False:
        ret_obj = ibmsecurity.isam.base.network.interfaces._get_interface(isamAppliance, label, vlanId)
        if ret_obj is not None:
            del ret_obj['objType']
            del ret_obj['type']
            json_data = {
                'uuid': ret_obj['uuid'],
                'name': name,
                'label': label,
                'comment': comment,
                'enabled': enabled,
                'vlanId': vlanId,
                'bondedTo': bondedTo,
                'bondingMode': bondingMode,
                'ipv4': {
                    'dhcp': ret_obj['ipv4']['dhcp'],
                    'addresses': ret_obj['ipv4']['addresses'],
                },
                'ipv6': {
                    'dhcp': ret_obj['ipv6']['dhcp'],
                    'addresses': ret_obj['ipv6']['addresses'],
                }
            }
            update_needed = not (
            ibmsecurity.utilities.tools.json_sort(ret_obj) == ibmsecurity.utilities.tools.json_sort(json_data))

        if force is True or update_needed is True:
            if check_mode is True:
                return isamAppliance.create_return_object(changed=True)
            else:
                return ibmsecurity.isam.base.network.interfaces._update_interface(isamAppliance, json_data)

    return isamAppliance.create_return_object()