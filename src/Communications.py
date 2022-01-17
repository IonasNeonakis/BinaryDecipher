class Communications:
    def __init__(self, apk):
        self._apk = apk

    def analyse(self):
        a, d, dx = self._apk
        permissions = a.get_permissions()
        print("PERMISSIONS DEMANDÉES : ", permissions)

        declared_permissions = a.declared_permissions()
        print("PERMISSIONS DECLARÉES : ", declared_permissions)
