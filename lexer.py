import numpy as np
import time

def proc_str(string):
    # Обезличивание переменных
    sep_words = ['+','-','*','/','^','(',')','{','}','\\','_',' ','&',',']
    f_string = ""
    i = 0
    while (i != len(string)):
        if string[i] == "\\":
            f_string += string[i]
            i += 1
            while (not(string[i] in sep_words)):
                f_string += string[i]
                i += 1
            i -= 1
        elif (string[i] in sep_words or string[i].isdigit() or string[i] == 'f' or string[i] == 'd'):
            f_string +=string[i]
        elif (string[i].isalpha()):
            f_string += '#'
        else:
            f_string +=string[i]
        i += 1

    return f_string

def jaccpp(str1, str2):
    # Расширенный коэффициент Жаккара
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1.intersection(set2))
    union = len(set1) + len(set2) - intersection
    return (intersection / union) * 100

def sert(str1, str2):
    # Дистанция Сёрта
    bigrams1 = {str1[i:i+2] for i in range(len(str1)-1)}
    bigrams2 = {str2[i:i+2] for i in range(len(str2)-1)}
    intersection = bigrams1.intersection(bigrams2)
    return (2 * len(intersection) / (len(bigrams1) + len(bigrams2))) * 100

def leven(str1, str2):
    # Расстояние Левенштейна 
    len_str1, len_str2 = len(str1), len(str2)
    matrix = np.zeros((len_str1 + 1, len_str2 + 1))

    for i in range(len_str1 + 1):
        matrix[i][0] = i
    for j in range(len_str2 + 1):
        matrix[0][j] = j
    for i in range(1, len_str1 + 1):
        for j in range(1, len_str2 + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            matrix[i][j] = min(matrix[i - 1][j] + 1,
                               matrix[i][j - 1] + 1,
                               matrix[i - 1][j - 1] + cost)

    lev_distance = matrix[len_str1][len_str2]
    max_len = max(len_str1, len_str2)
    return (1 - lev_distance / max_len) * 100

def coolPin(str1,str2):
    # Коэффициент Кульпина
    str1 = str1.replace('\f','\\f')
    str1 = str1.replace('\b','\\b')
    str1 = str1.replace('\t','\\t')
    str1 = str1.replace('\n','\\n')
    str1 = str1.replace('\r','\\r')

    str2 = str2.replace('\f','\\f')
    str2 = str2.replace('\b','\\b')
    str2 = str2.replace('\t','\\t')
    str2 = str2.replace('\n','\\n')
    str2 = str2.replace('\r','\\r')
    
    str1 = str1.replace('\\frac','')
    str2 = str2.replace('\\frac','')
    str1 = proc_str(str1)
    str2 = proc_str(str2)

    return ((leven(str1,str2) + jaccpp(str1,str2) + sert(str1,str2)) / 3)

def find_parts(str1, str2):
    # Нахождение общих подстрок и их фильтрация 
    common_substrings = []

    for i in range(len(str1)):
        for j in range(i + 1, len(str1) + 1):
            if str1[i:j] in str2:
                common_substrings.append(str1[i:j])
    all_values = sorted(list(set(common_substrings)))
    
    values = []
    max_len = -1
    for i in range (len(all_values)):
        if (len(all_values[i]) > max_len):
            max_len = len(all_values[i])
        elif (len(all_values[i]) <= max_len):
            values.append(all_values[i - 1])
            max_len = len(all_values[i])
    if len(all_values) != 0:
        values.append(all_values[-1])

    values = sorted(values,key = len, reverse = True)
    rm_cont = []
    for el1 in values:
        for el2 in values:
            if el1 != el2 and el2 in el1 or '#' not in el2:
                rm_cont.append(el2)
    for el1 in rm_cont:
        for el2 in values:
            if el2 == el1:
                values.remove(el2)

    return values

def replace_chars(base_string, pattern):
    # Взовращение переменным имени
    base_len = len(base_string)
    pattern_len = len(pattern)
    
    for i in range(base_len - pattern_len + 1):
        candidate = base_string[i:i + pattern_len]
        
        if all(c1 == c2 or c2 == '#' for c1, c2 in zip(candidate, pattern)):
            result = ''.join(c1 if c2 == '#' else c2 for c1, c2 in zip(candidate, pattern))
            return result
    return pattern

def fin_parts(s,v):
    # Массив с переменными в строку
    for i in range (len(v)):
        v[i] = replace_chars(s,v[i]).strip()
    return '$'.join(map(str, v))

def sparts(string1,string2):
    # Нахождение общих частей
    string1 = string1.replace('\f','\\f')
    string1 = string1.replace('\b','\\b')
    string1 = string1.replace('\t','\\t')
    string1 = string1.replace('\n','\\n')
    string1 = string1.replace('\r','\\r')

    string2 = string2.replace('\f','\\f')
    string2 = string2.replace('\b','\\b')
    string2 = string2.replace('\t','\\t')
    string2 = string2.replace('\n','\\n')
    string2 = string2.replace('\r','\\r')
    str1 = proc_str(string1)
    str2 = proc_str(string2)
    values = find_parts(str1 ,str2)
    values_c = values.copy()

    fstring = fin_parts(string1,values)
    sstring = fin_parts(string2,values_c)
    koef = (((len(fstring.replace("$","")) / len(string1)) *100 + (len(sstring.replace("$","")) / len(string2)) *100) / 2)
    # return str(int(koef)) + '@' + fstring + '@' + sstring
    return str(int(koef))


def main(in_string1,in_string2):
    start_time = time.time()
    a = coolPin(in_string1,in_string2)
    end_time = time.time()
    print("\nВремя коэфа Кульпина:",end_time - start_time )
    start_time = time.time()
    b = sparts(in_string1,in_string2)
    end_time = time.time()
    print("Время коэфа Ёлки:",end_time - start_time )
    print(f"Кульпин: {int(a)}")
    print(f"Ёлка: {b}\n")
     
    

if __name__ == "__main__":
    # Место для формул
    latex1 = "\frac{\sin(x+2)}{x + 51} * 5a + \log_a{xy + 2} + \log{x + 2} + \sqrt{a}"
    latex2 = "\log{a + 2} + \sqrt{x} + \log_x{ab + 2} + 5c + \frac{\sin(a+2)}{a + 51}"

    main(latex1,latex2)
    