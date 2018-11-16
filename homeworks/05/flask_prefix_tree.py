from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


class PrefixTree:
    def __init__(self):
        self.root = [{}]

    def add(self, string, node_item=None, periodicity=1):
        # добавить строку
        wrk_dict = self.root

        if self.check(string):
            for i in string:
                wrk_dict = wrk_dict[0][i]
            wrk_dict[1] += 1

        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                wrk_dict[0][i] = [{}]
                wrk_dict = wrk_dict[0][i]

        wrk_dict.append(periodicity)
        wrk_dict.append(node_item)

    def check(self, string):
        # проверить наличие строки
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                return False
        if len(wrk_dict) != 1:
            return True
        return False

    def check_part(self, string):
        # проверить наличие строки как префикса
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                return False
        return True

    def get_n_sag(self, string, n):
        # TODO возвращает массив
        top = []
        wrk_dict = self.root
        for i in string:
            if i in wrk_dict[0]:
                wrk_dict = wrk_dict[0][i]
            else:
                break

        if len(wrk_dict) != 0:
            top.append(string, wrk_dict[1], wrk_dict[2])

        def rec(t, wrk_d, st):
            for i in wrk_d[0]:
                st += i
                if len(wrk_dict[0][i]) != 0:
                    t.append(st, wrk_d[1], wrk_d[2])
                if len(wrk_d[0][i][0]) != 0:
                    rec(t, wrk_d[0][i], st)

        rec(top, wrk_dict, string)
        return top.sort(key=lambda x: x[1], reverse=True)[:n]

    """
        TODO реализация класса prefix tree, методы как на лекции + метод дать топ 10 продолжений.
        Скажем на строку кросс выдаем кроссовки, кроссовочки итп. Как хранить топ?
        Решать вам. Можно, конечно, обходить все ноды, но это долго.
        Дешевле чуток проиграть по памяти, зато отдавать быстро (скажем можно взять кучу)
        В терминальных (конечных) нодах может лежать json с топ актерами.
        """


def init_prefix_tree(filename):
    prefix_tree = PrefixTree()
    ar_to_el = []

    with open("./"+filename, "r") as file:
        for line in file:
            l = [i for i in line.split("\t")]
            ar_to_el.append(l)

    for line in ar_to_el:
        prefix_tree.add(line[0], line[1], line[2])

    return prefix_tree

    """
    TODO в данном методе загружаем данные из файла.
    Предположим вормат файла
                              "Строка, чтобы положить в дерево" \t
                              "json значение для ноды" \t
                               частота встречаемости
    """


@app.route("/get_sudgest/<string>", methods=['GET', 'POST'])
def return_sudgest(string):
    top = prefix_tree.get_n_sag(string, 10)
    for i in range(len(top)):
        top[i] = [top[i][0], top[i][2]]

    if request.method == "GET":
        return jsonify(top)

    # TODO по запросу string вернуть json, c топ-10 саджестами, и значениями из нод


@app.route("/")
def hello():
    return "Welcome on this server\nPlease go to /get_sudgest/"
    # TODO должна возвращатьс инструкция по работе с сервером


if __name__ == "__main__":
    prefix_tree = init_prefix_tree("For_tree.txt")
    app.run()
