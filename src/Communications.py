class Communications:
    def __init__(self, apk):
        self._apk = apk



    def analyse(self):
        a, d, dx = self._apk
        print('Permissions déclarées')
        permissions = a.get_permissions()
        print(permissions)
        print('Permissions Demandées')
