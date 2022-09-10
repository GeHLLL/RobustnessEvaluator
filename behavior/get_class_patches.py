import os
import json

import re

import utils

#infos_path = './config/infos.json'

mode = 'NV'

if mode == 'NV':
    buggy_lines_path = r'F:\workspace\bug_detection\data\Dataset_d4j\NewVariable\buggy_lines'
    buggy_methods_path = r'F:\workspace\bug_detection\data\Dataset_d4j\NewVariable\tab_methods'
    buggy_classes_path = r'F:\workspace\bug_detection\data\Dataset_d4j\NewVariable\buggy_classes'

if mode == 'trans':
    buggy_lines_path = r'F:\workspace\bug_detection\data\Dataset_d4j\trans_d4j\buggy_lines'
    buggy_methods_path = r'F:\workspace\bug_detection\data\Dataset_d4j\trans_d4j\tab_methods'
    buggy_classes_path = r'F:\workspace\bug_detection\data\Dataset_d4j\trans_d4j\buggy_classes'

if mode == 'raw':
    buggy_lines_path = r'F:\workspace\bug_detection\data\Dataset_d4j\buggy_lines'
    buggy_methods_path = r'F:\workspace\bug_detection\data\Dataset_d4j\tab_methods'
    buggy_classes_path = r'F:\workspace\bug_detection\data\Dataset_d4j\buggy_classes'

# def read_tab_method(path):
#     with open(path, encoding='utf-8') as fp:
#         lines = fp.readlines()
#     for i, line in enumerate(lines):
#         lines[i] = '    ' + line
#     return ''.join(lines)

def sequenceR():
    def restore(buggy_class, buggy_method, buggy_line, fix_line):
        assert buggy_line in buggy_method
        assert buggy_method in buggy_class
        new_method = buggy_method.replace(buggy_line, fix_line)
        new_class = buggy_class.replace(buggy_method, new_method)
        return new_class


    ids_path = r'F:\workspace\bug_detection\data\Dataset_d4j\NewVariable\patches\outputs_sequenceR\test.sids'
    patches_path = r'F:\workspace\bug_detection\data\Dataset_d4j\NewVariable\patches\outputs_sequenceR\sequenceR_raw.pred'

    ids = utils.read_lines(ids_path)
    patches = utils.read_lines(patches_path)

    result = {}

    for i, idx in enumerate(ids):
        if idx == 'Math---69---PearsonsCorrelation---m2---NewVariable---5':
            print()
        buggy_class = utils.my_read(os.path.join(buggy_classes_path, f'{idx}.java'))
        buggy_method = utils.my_read(os.path.join(buggy_methods_path, f'{idx}.txt'))
        buggy_line = utils.my_read(os.path.join(buggy_lines_path, f'{idx}.txt'))
        fix_line = patches[i]


        class_patch = restore(buggy_class, buggy_method, buggy_line, fix_line)

        result.update({idx: class_patch})

    return result


def tufano():
    #如果map读取失败，则返回原本的代码
    def replace_abs(map_path, code):
        with open(map_path, encoding='utf-8') as fp:
            try:
                data = json.load(fp)
            except Exception as e:
                return code

        for key, value in data.items():
            code = code.replace(value, key)

        return code

    def restore(buggy_class, buggy_method, fix_method):
        assert len(buggy_method) > 1
        assert buggy_method in buggy_class

        return buggy_class.replace(buggy_method, fix_method)

    path = r'F:\workspace\bug_detection\data\Dataset_d4j\patches\outputs_tufano'
    ids_path = os.path.join(path, 'test.sids')
    patches_path = os.path.join(path, 'Tufano_raw.pred')
    maps_path = r'F:\workspace\bug_detection\data\Dataset_d4j\patches\temps_tufano'

    ids = utils.read_lines(ids_path)
    patches = utils.read_lines(patches_path)

    result = {}

    for i, idx in enumerate(ids):
        map_path = os.path.join(maps_path, f'{idx}_buggy.txt.abs.map')
        buggy_class = utils.my_read(os.path.join(buggy_classes_path, f'{idx}.java'))
        buggy_method = utils.my_read(os.path.join(buggy_methods_path, f'{idx}.txt'))
        fix_method = patches[i]
        fix_method = replace_abs(map_path, fix_method)

        class_patch = restore(buggy_class, buggy_method, fix_method)

        result.update({idx: class_patch})

    return result


def recoder():
    def restore(buggy_class, buggy_method, fix_method):
        assert len(buggy_method) > 1
        assert buggy_method in buggy_class
        return buggy_class.replace(buggy_method, fix_method)

    path = r'F:\workspace\bug_detection\data\Dataset_d4j\NewVariable\patches'
    ids_path = os.path.join(path, 'new_recoder.ids')
    patches_path = os.path.join(path, 'outputs_recoder')

    ids = utils.read_lines(ids_path)

    result = {}
    for idx in ids:
        if idx == 'Math---69---PearsonsCorrelation---m2---NewVariable---5':
            print()
        buggy_class = utils.my_read(os.path.join(buggy_classes_path, f'{idx}.java'))
        buggy_method = utils.my_read(os.path.join(buggy_methods_path, f'{idx}.txt'))

        try:
            patch_data = utils.my_json_load(os.path.join(patches_path, f'{idx}.fix'))
        except Exception as e:
            print(e)
            continue
        fix_method = patch_data['0']
        if fix_method == 'error':
            continue
        else:
            if'\r\n' in fix_method:
                print(fix_method)
                fix_method = fix_method.replace('\r\n', '\n')
            class_patch = restore(buggy_class, buggy_method, fix_method)
            result.update({idx: class_patch})

    return result


def coconut(model_name):
    def token2statement(token_list, numbers, strings):
        flag_string_statements = 0
        ### if strings and numbers format of statement is [n1s1, n1s2, n1s3, n2s1, n2,s2, ...]
        if "$STRING$" in token_list and "$NUMBER$" in token_list:
            statements = [""] * len(strings) * len(numbers)
            flag_string_statements = 3
        elif "$NUMBER$" in token_list:
            statements = [""] * len(numbers)
            flag_string_statements = 2
        elif "$STRING$" in token_list:
            statements = [""] * len(strings)
            flag_string_statements = 1
        else:
            statements = [""]
        for i, token in enumerate(token_list):
            if i < len(token_list) - 1:
                # if token_list[i] == "or" or "and":
                #    for s in range(0, len(statements)):
                #        statements[s] += " " + token + " "
                if token_list[i] == "return":
                    if token_list[i + 1].isdigit() or token_list[i + 1] == "$NUMBER$":
                        for s in range(0, len(statements)):
                            statements[s] += token + " "
                    elif token_list[i + 1] == "CaMeL":
                        for s in range(0, len(statements)):
                            statements[s] += token
                    elif token_list[i + 1] == ".":  # no space
                        for s in range(0, len(statements)):
                            statements[s] += token
                    elif token_list[i + 1] == "(":  # Actually it does not seem to be needed.
                        for s in range(0, len(statements)):
                            statements[s] += " " + token
                    elif token_list[i + 1] == "_":  # no space
                        for s in range(0, len(statements)):
                            statements[s] += token
                    else:
                        for s in range(0, len(statements)):
                            statements[s] += token + " "

                elif token_list[i] == "$STRING$":
                    if flag_string_statements == 3:
                        for s in range(0, len(statements)):
                            if "'" not in strings[s % len(strings)]:
                                statements[s] += "'" + strings[s % len(strings)] + "'"
                            else:
                                statements[s] += '"' + strings[s % len(strings)] + '"'
                    elif flag_string_statements == 1:
                        for s in range(0, len(statements)):
                            if "'" not in strings[s]:
                                statements[s] += "'" + strings[s] + "'"
                            else:
                                statements[s] += '"' + strings[s] + '"'
                    else:
                        for s in range(0, len(statements)):
                            statements[s] += "'DEFAULT'"

                elif token_list[i] == "$NUMBER$":
                    if flag_string_statements == 3:
                        count = 0
                        # print("len_statemnt", len(statements))
                        for s in range(0, len(numbers)):
                            # print("s: ", len(numbers))
                            # print(len(statements))
                            # print(len(numbers)* len(strings) - 1 )
                            for stringlen in range(s, s + len(strings)):
                                statements[count] += numbers[s]
                                count += 1
                                # print("Count: ", count)

                    elif flag_string_statements == 2:
                        for s in range(0, len(statements)):
                            statements[s] += numbers[s]
                    else:
                        # use default number 2 (0 and 1 are specific tokens)
                        statements[s] += 2
                elif token_list[i] == "CaMeL":  # no space
                    pass
                elif token_list[i] == '*':
                    for s in range(0, len(statements)):
                        statements[s] += token
                elif token_list[i] == ".":  # no space
                    for s in range(0, len(statements)):
                        statements[s] += token
                elif token_list[i].isdigit():  # no space in general
                    if token_list[i + 1] == 'or' or token_list[i + 1] == 'and':
                        for s in range(0, len(statements)):
                            statements[s] += token + ' '
                    else:
                        for s in range(0, len(statements)):
                            statements[s] += token

                elif token_list[i] == "_":  # no space
                    for s in range(0, len(statements)):
                        statements[s] += token

                else:  # Default case"
                    if token_list[i + 1] == "CaMeL":  # no space
                        for s in range(0, len(statements)):
                            statements[s] += token
                    elif token_list[i + 1] == ".":  # no space
                        for s in range(0, len(statements)):
                            statements[s] += token
                    elif token_list[i + 1] == "(":  # Actually it does not seem to be needed.
                        for s in range(0, len(statements)):
                            statements[s] += token
                    elif token_list[i + 1] == "_":  # no space
                        for s in range(0, len(statements)):
                            statements[s] += token
                    elif token_list[i + 1].isdigit() or token_list[i + 1] == "$NUMBER$":  # no space
                        if token_list[i + 1] == 'or' or token_list[i + 1] == 'and':
                            for s in range(0, len(statements)):
                                statements[s] += token + " "
                        else:
                            for s in range(0, len(statements)):
                                statements[s] += token
                    else:
                        for s in range(0, len(statements)):
                            statements[s] += token + " "
            else:  # no space after the last statement
                for s in range(0, len(statements)):
                    statements[s] += token
        return statements
    def get_strings_numbers(string):
        # FIXME Does not work for s.append(',').append(',') return [',', ').append(', ',']
        matches1 = re.findall(r'(?<=\")(.*?)(?=\")', string)
        matches2 = re.findall(r"(?<=\')(.*?)(?=\')", string)
        strings = matches1 + matches2
        numbers = re.findall(r'\d+', string)
        return strings, numbers
    def Recovery_CoCoNut_one(buggy_str, pred_str):
        strings, numbers = get_strings_numbers(buggy_str)
        recovery_tokens = pred_str.split()
        recovery_str = token2statement(recovery_tokens, numbers, strings)
        # print(recovery_str)
        if len(recovery_str) == 0:
            recovery_str = [pred_str]
        return recovery_str[0]

    def restore(buggy_class, buggy_method, buggy_line, fix_line):
        assert buggy_line in buggy_method
        assert buggy_method in buggy_class
        return buggy_class.replace(buggy_method, buggy_method.replace(buggy_line, fix_line))


    ids_path = r'F:\workspace\bug_detection\data\Dataset_d4j\NewVariable\ids.txt'
    patches_path = rf'F:\workspace\bug_detection\data\Dataset_d4j\NewVariable\patches\outputs_CoCoNut\{model_name}.result'
    buggy_lines_path = r'F:\workspace\bug_detection\data\Dataset_d4j\NewVariable\buggy_lines'

    ids = utils.read_lines(ids_path)
    patches = utils.my_json_load(patches_path)

    result = {}
    for pos, fix_line in patches.items():
        idx = ids[int(pos)]
        if idx == 'Math---69---PearsonsCorrelation---m2---NewVariable---5':
            print()
        buggy_class = utils.my_read(os.path.join(buggy_classes_path, f'{idx}.java'))
        buggy_method = utils.my_read(os.path.join(buggy_methods_path, f'{idx}.txt'))
        buggy_line: str = utils.my_read(os.path.join(buggy_lines_path, f'{idx}.txt'))
        fix_line = Recovery_CoCoNut_one(buggy_line, fix_line[0])

        class_patch = restore(buggy_class, buggy_method, buggy_line, fix_line)
        result.update({idx: class_patch})

    return result




if __name__ == '__main__':
    # path = r'F:\workspace\bug_detection\data\Dataset_d4j\NewVariable\patches\outputs_CoCoNut'
    # files = [file for file in os.listdir(path) if file.endswith('.result')]
    # for file in files:
    #     model_name = file.replace('.result', '')
    #     result = coconut(model_name)
    #
    #     with open(f'./patches/{model_name}.patches', 'w', encoding='utf-8') as fp:
    #         json.dump(result, fp, ensure_ascii=False, indent=4)
    #     break

    result = sequenceR()

    with open(f'./patches/sequenceR_NV.patches', 'w', encoding='utf-8') as fp:
        json.dump(result, fp, ensure_ascii=False, indent=4)