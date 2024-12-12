import time

var_dict = {}
clear_var_dict = {}
const_dict = {}
clear_const_dict = {}
sep_words = ['+','-','*','/','^','(',')','{','}','[',']','\\','_',' ','&',',']
greek_words = ['\\alpha','\\beta','\\Gamma','\\gamma','\\Delta','\\delta','\\epsilon','\\varepsilon','\\zeta','\\eta'
    ,'\\Theta','\\theta','\\vartheta','\\iota','\\kappa','\\varkappa','\\Lambda','\\lambda','\\mu','\\nu','\\Xi','\\xi'
    ,'\\Pi','\\pi','\\varpi','\\rho','\\varrho','\\Sigma','\\sigma','\\varsigma','\\tau','\\Upsilon','\\upsilon','\\Phi'
    ,'\\phi','\\varphi','\\chi','\\Psi','\\psi','\\Omega','\\omega']

# Обезличивание греческих букв
def proc_greek_str(string):
    for word in greek_words:
        idx = string.find(word)
        while idx != -1:
            string = string[:idx] + '#' + string[idx + len(word):]
            var_dict[idx] = word
            idx = string.find(word, idx + 1)

    return string

# Обезличивание переменных и констант
def proc_str(string):
    string += ' '    
    proc_string = ""
    i = 0
    # Замена переменных и констант на # и @ соответственно
    while (i != len(string)):
        if string[i] == "\\":
            proc_string += string[i]
            i += 1
            while (not(string[i] in sep_words)):
                proc_string += string[i]
                i += 1
            i -= 1
        elif (string[i] in sep_words or string[i] == 'f' or string[i] == 'd'):
            proc_string +=string[i]
        elif (string[i].isalpha()):
            proc_string += '#'
        elif (string[i].isdigit()):
            proc_string += '@'
        else:
            proc_string +=string[i]
        i += 1
    # Замена греческих букв
    proc_string = proc_greek_str(proc_string).strip()
    # Удаление повторяющихся @
    result = proc_string[0]
    for char in proc_string[1:]:
        if char != '@' or result[-1] != '@':
            result += char

    return result

# Нахождение общих подстрок и их фильтрация 
def find_parts(str1, str2):
    common_substrings = []
    # Нахождение всех схожих подстрок
    for i in range(len(str1)):
        for j in range(i + 1, len(str1) + 1):
            if str1[i:j] in str2:
                common_substrings.append(str1[i:j])
    all_templates = sorted(list(set(common_substrings)))
    
    templates = []
    max_len = -1
    # Сортировка подстрок по длинне
    for i in range (len(all_templates)):
        if (len(all_templates[i]) > max_len):
            max_len = len(all_templates[i])
        elif (len(all_templates[i]) <= max_len):
            templates.append(all_templates[i - 1])
            max_len = len(all_templates[i])
    if len(all_templates) != 0:
        templates.append(all_templates[-1])

    key_words = ['#','@']
    templates = sorted(templates,key = len, reverse = True)
    rm_temp = []
    # Нахождение неуникальных строк
    for el1 in templates:
        for el2 in templates:
            if (el1 != el2 and el2 in el1) or all(word not in el2 for word in key_words):
                rm_temp.append(el2)
    # Удаление неуникальных строк
    for el1 in rm_temp:
        for el2 in templates:
            if el2 == el1:
                templates.remove(el2)

    return templates

# Формирование словарей для подстановки переменных и констант
def make_dicts(string,str_temp):
    var_dict.clear()
    const_dict.clear()
    clear_var_dict.clear()
    clear_const_dict.clear()
    
    string += ' '    
    i = 0
    # Нахождение индексов всех переменных и констант
    while (i != len(string)):
        if string[i] == "\\":
            i += 1
            while (not(string[i] in sep_words)):
                i += 1
            i -= 1
        elif (string[i] in sep_words or string[i] == 'f' or string[i] == 'd'):
            i = i
        elif (string[i].isalpha()):
            var_dict[i] = string[i]
        elif (string[i].isdigit()):
            const_dict[i] = string[i]
        else:
            i = i
        i += 1
    # Обработка греческих символов
    proc_greek_str(string)
    # Объединение констант в одно число, если они им являются 
    for key in sorted(const_dict, reverse=True):
        if key - 1 in const_dict:
            const_dict[key - 1] = const_dict[key - 1] + const_dict[key]
            del const_dict[key]
    # Корректировка словоря констант по индексам
    list_temp = list(str_temp)
    for key in sorted(const_dict):
        for i in range (len(str_temp)):
            if list_temp[i] == '@':
                clear_const_dict[i] = const_dict[key]
                list_temp[i] = ''
                break
    # Корректировка словоря переменных по индексам
    for key in sorted(var_dict):
        for i in range (len(str_temp)):
            if list_temp[i] == '#':
                clear_var_dict[i] = var_dict[key]
                list_temp[i] = ''
                break
    
# Взовращение переменным и константам имена
def replace_chars(template,str_temp):
    list_temp = list(template)
    temp_idx = str_temp.find(template)
    temp_size = temp_idx + len(list_temp)
    # Работа с переменными
    for idx,var in clear_var_dict.items():
        if idx >= temp_idx and idx < temp_size:
            list_temp[idx - temp_idx] = var
    # Работа с константами
    for idx,const in clear_const_dict.items():
        if idx >= temp_idx and idx < temp_size:
            list_temp[idx - temp_idx] = const
    
    return ''.join(list_temp)

# Массив с переменными в строку
def fin_parts(string,str_temp,templates):
    make_dicts(string,str_temp)
    for i in range (len(templates)):
        templates[i] = replace_chars(templates[i].strip(),str_temp)
    return '$'.join(templates)
    
# Нахождение общих частей
def sparts(string1,string2):
    replacements = {'\a' : '\\a','\b' : '\\b','\c' : '\\c','\d' : '\\d','\e' : '\\e','\f' : '\\f','\g' : '\\g'
    ,'\h' : '\\h','\i' : '\\i','\j' : '\\j','\k' : '\\k','\l' : '\\l','\m' : '\\m','\n' : '\\n','\p' : '\\p'
    ,'\o' : '\\o','\q' : '\\q','\r' : '\\r','\s' : '\\s','\t' : '\\t','\v' : '\\v','\w' : '\\w'
    ,'\y' : '\\y'}
    # Корректировка строк
    for old, new in replacements.items():
        string1 = string1.replace(old, new)
        string2 = string2.replace(old, new)
    # Обработка строк обезличиванием переменных
    str1, str2 = proc_str(string1).strip(),proc_str(string2).strip()
    # Нахождение общих частей
    templates = find_parts(str1 ,str2)
    templates_c = templates.copy()
    # Подстановка переменных и констант в схожие части
    same_parts_string1, same_parts_string2 = fin_parts(string1,str1,templates), fin_parts(string2,str2,templates_c)
    # Вычисление коэфициента схожести
    koef = (((len(same_parts_string1.replace("$","")) / len(string1)) *100 + (len(same_parts_string2.replace("$","")) / len(string2)) *100) / 2)
    return str(int(koef)) + '\n\n' + same_parts_string1.replace("$","\n") + '\n\n' + same_parts_string2.replace("$","\n")
    # return str(int(koef))


def main(in_string1,in_string2):
    start_time = time.time()
    b = sparts(in_string1,in_string2)
    end_time = time.time()
    print("Время коэфа Ёлки:",end_time - start_time )
    print(f"Ёлка: {b}\n")
     
    

if __name__ == "__main__":
    # Место для формул
    latex1 = "\alpha + \beta = \gamma"
    latex2 = "\alpha + \beta + \delta = \gamma"
    main(latex1,latex2)
    