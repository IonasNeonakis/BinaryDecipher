from itertools import chain


class Communications:
    def __init__(self, apk):
        self._apk = apk

    def analyse(self):
        a, d, dx = self._apk
        permissions = a.get_permissions()
        print("PERMISSIONS", permissions)


"""
        for meth, perm in dx.get_permissions(a.get_effective_target_sdk_version()):
            print("Using API method {} for permission {}".format(meth, perm))
            print('used in:')
            for _, m, _ in meth.get_xref_from():
                print(m.full_name)
        
        for meth in dx.get_permission_usage("android.permission.ACCESS_FINE_LOCATION", a.get_effective_target_sdk_version()):
            print("Using API method {}".format(meth))
            print("used in:")
            for _, m, _ in meth.get_xref_from():
                print(m.full_name)
"""
'''
        for meth in dx.get_permission_usage(‘android.permission.SEND_SMS’, a.get_effective_target_sdk_version()):
            print(“Using APImethod
            {}”.format(meth)) print(“used in:”) for _, m, _ in meth.get_xref_from():

        print(m.full_name)

        print('Permissions déclarées')
        permissions = a.get_permissions()
        print(permissions)
        print('Permissions Demandées')
'''

#