from pysnmp import hlapi

def get(target, oids, credentials, port = 161, engine = hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(engine, hlapi.CommunityData(credentials), hlapi.UdpTransportTarget((target, port)), context, *construct_object_types(oids))
    return fetch(handler, 1) [0]

def construct_object_types(list_of_oids):
    object_types = []

    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))

    return object_types

def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError("got SNMP error: {0}" .format(error_indication))
        except StopIteration:
            break
    return result


def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value