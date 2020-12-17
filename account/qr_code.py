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
    all_actions = ['cashier', 'add_point', 'make_point_card',
                   'use_stamp', 'use_point', 'add_stamp']

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
        qr = str(','.join([self.user_type, str(self.pk), *self.action]))
        return self.make_qr_format(string=qr)

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

        string_list = cls.parse_qr_format(qr_data=string).split(',')
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


    def make_qr_format(self,string):
        i = 0
        string_list = string.split(',')
        qr_format_list = []
        for c in string_list:
            if i == 0:
                if c == 'Customer':
                    qr_format_list.append(0)
                elif c == 'Shop':
                    qr_format_list.append(1)
                else:
                    raise QRCodeError
            elif i == 1:
                qr_format_list.append(c)
                qr_format_list.append('-')
            else:
                if c in self.all_actions:
                    qr_format_list.append(self.all_actions.index(c))
                else:
                    raise QRCodeError
            
            i+=1
        
        return ''.join(map(str,qr_format_list))

    @classmethod
    def parse_qr_format(cls,qr_data):
        i = 0
        check = 0
        qr_string = []
        qr_pk = []
        for c in qr_data:
            if i == 0:
                if c == '0':
                    qr_string.append('Customer')
                    print(qr_string)
                elif c == '1':
                    qr_string.append('Shop')
                    print(qr_string)
                else:
                    raise QRCodeError
            else:
                if check == 0:
                    if c != '-':
                        qr_pk.append(c)
                    else:
                        qr_string.append(''.join(qr_pk))
                        check = 1
                else:
                    if c == '0':
                        qr_string.append(cls.all_actions[0])
                    elif c == '1':
                        qr_string.append(cls.all_actions[1])
                    elif c == '2':
                        qr_string.append(cls.all_actions[2])
                    elif c == '3':
                        qr_string.append(cls.all_actions[3])
                    elif c == '4':
                        qr_string.append(cls.all_actions[4])
                    elif c == '5':
                        qr_string.append(cls.all_actions[5])
                    else:
                        raise QRCodeError
 
            i+=1 
        return ','.join(qr_string)

        
    



