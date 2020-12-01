from account.models import User


class QRCodeError(Exception):
    pass


class InvalidUserTypeError(QRCodeError):
    pass


class InvalidPkError(QRCodeError):
    pass


class InvalidActionError(QRCodeError):
    pass


class QRCode:
    all_actions = ['cashier', 'add_point', 'make_point_card', 'use_stamp']

    def __init__(self, user_type, pk, action=all_actions):
        #user_type
        if not user_type in {'Customer', 'Shop'}:
            raise InvalidUserTypeError
        self.user_type = user_type
        #pk
        try:
            pk = int(pk)
        except:
            raise InvalidPkError
        if not User.objects.filter(pk=pk).exists():
            raise InvalidPkError
        if user_type == 'Customer':
            if not User.objects.get(pk=pk).is_customer:
                raise InvalidPkError
        else:
            if not User.objects.get(pk=pk).is_shop:
                raise InvalidPkError
        self.pk = pk
        #action
        for a in action:
            if not a in self.all_actions:
                raise InvalidActionError
        self.action = action

    def __str__(self):
        return ','.join([self.user_type, str(self.pk), *self.action])

    @classmethod
    def from_user(cls, user, action=all_actions):
        if user.is_customer:
            return cls('Customer', user.pk, action)
        elif user.is_shop:
            return cls('Shop', user.pk, action)
        else:
            raise InvalidUserTypeError

    @classmethod
    def from_str(cls, string):

        string_list = string.split(',')
        if len(string_list) < 2:
            raise QRCodeError
        if len(string_list) > 2:
            return cls(string_list[0], string_list[1], string_list[2:])
        else:
            return cls(*string_list)

    @classmethod
    def _is_valid(cls, qr_string):
        qr_string_list = qr_string.split(',')

        if len(qr_string_list) < 2:
            return False

        if qr_string_list[0] in {'Customer', 'Shop'}:
            return False

        pk = qr_string_list[1]
        try:
            pk = int(pk)
        except:
            return False
        if not User.objects.filter(pk=pk).exists():
            return False

        if len(qr_string_list) >= 3:
            for i in range(2, len(qr_string_list)):
                if not qr_string_list[i] in cls.all_actions:
                    return False

        return True
