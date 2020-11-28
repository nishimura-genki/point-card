class QRCode:
    def __init__(self, user_type, pk, action=None):
        assert user_type in {'Customer', 'Shop'}
        self.user_type = user_type
        self.pk = int(pk)
        self.action = action

    def __str__(self):
        if action == None:
            return ','.join([self.user_type, self.pk, ])
        else:
            return ','.join([self.user_type, self.pk, self.action])

    @classmethod
    def from_user(cls, user, action=None):
        if user.is_customer:
            return cls('Customer', user.pk)
        elif user.is_shop:
            return cls('Shop', user.pk)
        else:
            raise Exception()

    @classmethod
    def from_str(cls, string):
        return cls(*string.split(','))
