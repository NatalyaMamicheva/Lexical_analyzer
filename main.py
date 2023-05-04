import re

import pandas as pd

try:
    with open("data.txt", "r", encoding='UTF-8') as table:
        with open("code.txt", "r", encoding='UTF-8') as co:
            with open("file_end.txt", "w", encoding='UTF-8') as output:
                input_data = table.read().replace('\n', " ").split()
                index_data = input_data.index("NE")
                data_tl = input_data[index_data:]
                data_tw = input_data[:index_data]
                code_data = co.read().replace('\n', " ").split()

                # Комментарии
                if '.' not in code_data:
                    op = code_data.index('(*')
                    en = code_data.index('*)')
                    op_ind = (code_data[:op + 1])
                    en_ind = (code_data[en:])
                    code_data = op_ind + en_ind

                # Выход из программы после точки
                list_element = []
                list_words = []
                join_elements = []

                for all in code_data:
                    list_element.append(list(all))

                for i in list_element:
                    for el in i:
                        list_words.append(el)
                        if el == '.':
                            index_end_coder = list_element.index(i)
                            del list_element[index_end_coder:]

                for i in list_words:
                    if i == '.':
                        index_end_code = list_words.index(".")
                        del list_words[index_end_code:]

                end_list = []
                for end in list_element:
                    for e in end:
                        end_list.append(e)

                for end in list_element:
                    join_elements.append(''.join(end))

                e = len(end_list)
                list_difference = (list_words[e:])
                list_element.append(list_difference)

                code_data = []
                for i in list_element:
                    p = "".join(i)
                    code_data.append(p)

                nums = []

                # Вывод вещественных чисел
                # for all in code_data:
                #     num_float = re.findall("\d+\.\d+", all)
                #     if len(num_float) > 0:
                #         for all_float in num_float:
                #             nums.append(all_float)
                #             code_data.pop(code_data.index(all_float))

                # Вывод экспоненциальных чисел и их порядка
                for all in code_data:
                    num = re.findall('[-+]?[0-9]+', all)
                    let = re.findall('[E]', all)
                    sign = re.findall('[-+]', all)
                    if (let) and (num) and (sign):
                        need = num[0] + let[0] + num[-1]
                        try:
                            if all == need:
                                nums.append(all)
                                code_data.pop(code_data.index(all))
                        except:
                            pass

                # Вывод шестнадцатеричных чисел
                for all in code_data:
                    num = re.findall('[-+]?[0-9]+', all)
                    let = re.findall('[ABCDEF]', all)
                    if (num) and (let):
                        need = num[0] + ''.join(let)
                        try:
                            if all == need:
                                nums.append(all)
                                code_data.pop(code_data.index(all))
                        except:
                            pass

                # Вывод целых чисел
                for all in code_data:
                    num_int = re.findall('[-+]?[0-9]+', all)
                    if len(num_int) > 0:
                        for all_int in num_int:
                            nums.append(all_int)
                            code_data.pop(code_data.index(all_int))
                set_floatint = (list(set(filter(None, nums))))

                # Вывод служебных слов
                tw_words = []
                for all in code_data:
                    if len(all) > 1:
                        reg = re.compile('[^A-Z ]')
                        upper_letters = reg.sub('', all)
                        tw_words.append(upper_letters)
                        excep = ['PLUS', 'MULT', 'GT']
                        for e in excep:
                            if e in tw_words:
                                del tw_words[tw_words.index(e)]
                all_upper = (list(filter(None, tw_words)))
                set_upper = (list(set(filter(None, tw_words))))
                for u in all_upper:
                    code_data.pop(code_data.index(u))

                # Вывод идентификаторов
                ti = []
                for all in code_data:
                    if len(all) == 1:
                        reg = re.compile('[^a-zA-Z ]')
                        lower_letters = reg.sub('', all)
                        ti.append(lower_letters)
                all_lower = (list(filter(None, ti)))
                set_lower = (list(set(filter(None, ti))))
                for l in all_lower:
                    code_data.pop(code_data.index(l))

                # Вывод разделителей
                set_tl = (list(set(filter(None, code_data))))

                # Вывод знака переноса строки
                for all in code_data:
                    if ("\n" in all):
                        set_tl.append(all)

                # Запись в таблицу служебных слов TW(1)
                tw_tw = list(set(set_upper + data_tw))
                tw = pd.DataFrame({'TW 1': tw_tw})
                output.write(f"{tw.to_string()}\n")

                # Запись в таблицу разделителей TL(2)
                tl_tl = list(set(set_tl + data_tl))
                tl = pd.DataFrame({'TL 2': tl_tl})
                output.write(f"{tl.to_string()}\n")

                # Запись в таблицу чисел TN(3)
                tn_tn = pd.DataFrame({'TN 3': set_floatint})
                output.write(f"{tn_tn.to_string()}\n")

                # Запись в таблицу идентификаторов TI(4)
                ti_ti = pd.DataFrame({'TI 4': set_lower})
                output.write(f"{ti_ti.to_string()}\n")

                lex = []
                # Получение пар лексем служебных слов
                for i, val in enumerate(tw_tw, start=0):
                    # output.write(f'(0,{i}) => {val}\n')
                    lex.append([1, i, val])

                # Получение пар лексем разделителей
                for i, val in enumerate(tl_tl, start=0):
                    # output.write(f'(1,{i}) => {val}\n')
                    lex.append([2, i, val])

                # Получение пар лексем чисел
                for i, val in enumerate(set_floatint, start=0):
                    # output.write(f'(2,{i}) => {val}\n')
                    lex.append([3, i, val])

                # Получение пар лексем идентификаторов
                for i, val in enumerate(set_lower, start=0):
                    # output.write(f'(3,{i}) => {val}\n')
                    lex.append([4, i, val])

    # Получение пар лексем по коду из текстового файла
    with open("code.txt", "r", encoding='UTF-8') as co:
        with open("file_end.txt", "a", encoding='UTF-8') as output:
            code_data = co.read().replace('\n', " ").split()

            list_element = []
            list_words = []
            join_elements = []

            for all in code_data:
                list_element.append(list(all))

            for i in list_element:
                for el in i:
                    list_words.append(el)
                    if el == '.':
                        index_end_coder = list_element.index(i)
                        del list_element[index_end_coder:]

            for i in list_words:
                if i == '.':
                    index_end_code = list_words.index(".")
                    del list_words[index_end_code:]

            end_list = []
            for end in list_element:
                for e in end:
                    end_list.append(e)

            for end in list_element:
                join_elements.append(''.join(end))

            e = len(end_list)
            list_difference = (list_words[e:])
            list_element.append(list_difference)

            code_data = []
            for i in list_element:
                p = "".join(i)
                code_data.append(p)

            for l in code_data:
                b = 0
                while b < len(lex):
                    if l in lex[b] and l != '.':
                        output.write(f'({lex[b][0]},{lex[b][1]})\n')
                    if i == ".":
                        index_end_code = code_data.index(".")
                        del code_data[index_end_code:]
                        break
                    b += 1
            print("Лексический анализ успешно завершен!")

except ValueError:
    print('Ошибка! Завершение анализа.')
