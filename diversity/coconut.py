import os
import re
from typing import List
import datetime
from javalang import tokenizer
import json


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


def my_read(path):
    with open(path, encoding='utf-8') as fp:
        return fp.read()
def read_lines(path):
    with open(path, encoding='utf-8') as fp:
        lines = fp.readlines()
    lines = [line.strip() for line in lines]
    return lines

def get_no_space(str):
    return re.sub('\s+', '', str)



def fix_test(fix_line, buggy_line, preds, model='raw', raw=None, rep=None):
    assert model in ['raw', 'ChangeName', 'AddCast']

    fix_line = get_no_space(fix_line)
    if model == 'raw':
        for pred in preds:
            pred = Recovery_CoCoNut_one(buggy_line, pred)
            pred = get_no_space(pred)
            if pred == fix_line:
                return True

    if model == 'ChangeName':
        def restore(tokens, raw, rep):
            for i, token in enumerate(tokens):
                if token == raw:
                    tokens[i] = rep
            return tokens

        for pred in preds:
            pred = Recovery_CoCoNut_one(buggy_line, pred)
            pred = pred.split()
            pred = restore(pred, rep, raw)
            pred = ''.join(pred)
            pred = get_no_space(pred)

            if pred == fix_line:
                return True

    if model == "AddCast":
        for pred in preds:
            pred = Recovery_CoCoNut_one(buggy_line, pred)
            pred = get_no_space(pred)
            rep = get_no_space(rep)
            pred.replace(rep, raw)
            if pred == fix_line:
                return True

    return False
def fix_test1(fix_line, buggy_line, preds, model='raw', raw=None, rep=None):
    assert model in ['raw', 'ChangeName', 'AddCast']

    fix_line = get_no_space(fix_line)
    if model == 'raw':
        for pred in preds:
            pred = Recovery_CoCoNut_one(buggy_line, pred)
            pred = get_no_space(pred)
            if pred == fix_line:
                return True

    if model == 'ChangeName':
        def get_tokens(code):
            tokens = list(tokenizer.tokenize(code))
            tokens = [t.value for t in tokens]
            return tokens
        def restore(tokens, raw, rep):
            for i, token in enumerate(tokens):
                if token == raw:
                    tokens[i] = rep
            return tokens

        for pred in preds:
            pred = Recovery_CoCoNut_one(buggy_line, pred)
            #pred = pred.split()
            try:
                pred = get_tokens(pred)
            except Exception as e:
                continue
            pred = restore(pred, rep, raw)
            pred = ''.join(pred)
            pred = get_no_space(pred)

            if pred == fix_line:
                return True

    if model == "AddCast":
        for pred in preds:
            pred = Recovery_CoCoNut_one(buggy_line, pred)
            pred = get_no_space(pred)
            rep = get_no_space(rep)
            pred.replace(rep, raw)
            if pred == fix_line:
                return True

    return False

def xxx():
    output_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\patches\outputs_CoCoNut'
    ids_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\ids.txt'

    changes_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\changes'
    fix_lines_path = r'F:\workspace\bug_detection\data\Dataset\fixed_lines'
    buggy_lines_path = r'F:\workspace\bug_detection\data\Dataset\buggy_lines'

    model_name = 'CoCoNut_12'
    pred_path = os.path.join(output_path, f'{model_name}_b100.result')

    ids = read_lines(ids_path)
    with open(pred_path, encoding='utf-8') as fp:
        result = json.load(fp)

    i=0
    count = 0
    id_dir = {}
    for pos, preds in result.items():
        id_with_trans = ids[int(pos)]
        if not id_with_trans == '61791f7a1f6e65eedfc70e1a---ChangeName---1':
            continue
        infos = id_with_trans.split('---')
        idx = infos[0]

        if not idx in id_dir:
            id_dir[idx] = {}

        fix_line = os.path.join(fix_lines_path, f'{idx}.txt')
        fix_line = my_read(fix_line)
        buggy_line = os.path.join(buggy_lines_path, f'{idx}.txt')
        buggy_line = my_read(buggy_line)

        success = None
        if len(infos) == 1:
            success = fix_test(fix_line, buggy_line, preds)
        else:
            change_path = os.path.join(changes_path, f'{id_with_trans}.txt')
            change = my_read(change_path)
            change = change.split('->')
            success = fix_test(fix_line, buggy_line, preds, model=infos[1], raw=change[0], rep=change[1])

        id_dir[idx][id_with_trans] = success

        if success:
            count += 1
        i += 1
        if i % 100 == 0:
            print(f'{i} / {len(ids)}, count: {count}')

def main():
    output_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\patches\outputs_CoCoNut'
    ids_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\ids.txt'

    changes_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\changes'
    fix_lines_path = r'F:\workspace\bug_detection\data\Dataset\fixed_lines'
    buggy_lines_path = r'F:\workspace\bug_detection\data\Dataset\buggy_lines'


    models = os.listdir(output_path)
    models = [file.split('.')[0] for file in models if file.endswith('.result')]
    for model_name in models:
        #model_name = 'CoCoNut_12'

        pred_path = os.path.join(output_path, f'{model_name}.result')

        ids = read_lines(ids_path)
        with open(pred_path, encoding='utf-8') as fp:
            result = json.load(fp)

        id_dir = {}
        i = 0
        count = 0
        for pos, preds in result.items():
            id_with_trans = ids[int(pos)]
            infos = id_with_trans.split('---')
            idx = infos[0]
            if not id_with_trans == '61791f7a1f6e65eedfc70e1a---ChangeName---1':
                continue
            if not idx in id_dir:
                id_dir[idx] = {}

            fix_line = os.path.join(fix_lines_path, f'{idx}.txt')
            fix_line = my_read(fix_line)
            buggy_line = os.path.join(buggy_lines_path, f'{idx}.txt')
            buggy_line = my_read(buggy_line)

            success = None
            if len(infos) == 1:
                success = fix_test1(fix_line, buggy_line, preds)
            else:

                change_path = os.path.join(changes_path, f'{id_with_trans}.txt')
                change = my_read(change_path)
                change = change.split('->')
                success = fix_test1(fix_line, buggy_line, preds, model=infos[1], raw=change[0], rep=change[1])

            id_dir[idx][id_with_trans] = success

            if success:
                count += 1
            i += 1
            if i % 100 == 0:
                print(f'{i} / {len(ids)}, count: {count}')


        with open(f'./result/{model_name}_result_new_{datetime.date.today()}.json', 'w', encoding='utf-8') as fp:
            json.dump(id_dir, fp, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()








