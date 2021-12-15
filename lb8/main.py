from models import Model
import const


def answer():
    for key, value in const.MENU.items():
        if type(value) == list:
            print(f"{key} - {value[0]}")
        else:
            print(f"{key} - {value}")
    answer = input().lower()
    return answer


def new_answer():
    for key, value in const.MENU[answer][1].items():
        print(f"{key} - {value}")
    new_answer = input().lower()
    return new_answer


class Bank(object):

    def __init__(self):
        self.model = Model()

    def set_users(self):
        first_name, last_name = map(str, input("Введите имя и фамилию: ").split(" "))
        age = int(input("Введите ваш возраст: "))
        sex = input("Введите ваш пол: ")
        while sex not in const.SEX.keys():
            sex = input("Введите ваш пол (Мужской или Женский): ")
        self.model.set_user(
            first_name=first_name,
            last_name=last_name,
            age=age,
            sex=const.SEX[sex],
            money=0
        )

    def get_all_users(self):
        results = self.model.get_all_users()
        for result in results:
            print(dict(result))

    def get_one_user(self):
        user_id = input("Введите id пользователя: ")
        print(self.model.get_one_user(user_id))

    def update_one_user(self):
        user_id = input("Введите id пользователя: ")
        print(self.model.get_one_user(user_id))
        phone = input("Введите мобильный номер: ")
        email = input("Введите вашу почту: ")
        self.model.update_one_user(
            user_id=user_id, phone=phone, email=email
        )
        results = self.model.get_more_inform_one_user(user_id)
        for result in results:
            print(dict(result))

    def add_money(self, type_oper):
        user_id = input("Введите id пользователя: ")
        money = float(input("Введите сумму пополнения: "))
        type_oper = const.OPER_TYPE[type_oper]
        self.model.add_or_out_money(user_id, money, type_oper)

    def cash_out(self, type_oper):
        user_id = input("Введите id пользователя: ")
        money = float(input("Введите сумму снятия: "))
        type_oper = const.OPER_TYPE[type_oper]
        self.model.add_or_out_money(user_id, money, type_oper)

    def trans_money(self, type_oper):
        user_id = input("Введите id пользователя: ")
        user_id_tran = input("Введиет id получателя: ")
        money = float(input("Введите сумму перевода: "))
        type_oper = const.OPER_TYPE[type_oper]
        self.model.trans_money(user_id, user_id_tran, money, type_oper)

    def del_user(self):
        user_id = input("Введите id пользователя: ")
        self.model.del_user(user_id)

    def del_all_users(self):
        self.model.del_user()

    def del_last_entry(self):
        self.model.del_last_entry()

    def del_all_entry_user(self, oper):
        user_id = None
        if oper:
            user_id = input("Введите id пользователя: ")
        self.model.del_all_entry_user(user_id)


if __name__ == "__main__":
    print("Добро пожаловать")
    bank = Bank()
    answer = answer()
    while answer != "e":
        if answer == "a":
            bank.set_users()
        elif answer == "b":
            new_answer = new_answer()
            while new_answer != "e":
                if new_answer == "f":
                    bank.get_all_users()
                elif new_answer == "g":
                    bank.get_one_user()
                elif new_answer == "h":
                    bank.update_one_user()
                new_answer = new_answer()
        elif answer == "c":
            new_answer = new_answer()
            while new_answer != "e":
                if new_answer == "f":
                    bank.get_all_users()
                    type_oper = const.MENU[answer][1][new_answer]
                    bank.add_money(type_oper)
                elif new_answer == "g":
                    bank.get_all_users()
                    type_oper = const.MENU[answer][1][new_answer]
                    bank.cash_out(type_oper)
                elif new_answer == "h":
                    bank.get_all_users()
                    type_oper = const.MENU[answer][1][new_answer]
                    bank.trans_money(type_oper)
                new_answer = new_answer()
        elif answer == "d":
            new_answer = new_answer()
            while new_answer != "e":
                if new_answer == "f":
                    bank.get_all_users()
                    bank.del_user()
                elif new_answer == "g":
                    bank.del_all_users()
                    bank.get_all_users()
                elif new_answer == "h":
                    bank.del_last_entry()
                elif new_answer == "j":
                    bank.del_all_entry_user(oper=True)
                elif new_answer == "k":
                    bank.del_all_entry_user(oper=False)
                new_answer = new_answer()
        answer = answer()




