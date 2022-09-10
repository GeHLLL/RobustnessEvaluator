import os
import json
import re
from javalang import tokenizer


def read_files(path):
    with open(path, encoding='utf-8') as fp:
        data = fp.readlines()
    data = [line.strip() for line in data]
    return data


def fix_test(fix_line, preds, model='raw', raw=None, rep=None):

    if model == 'raw':
        fix_line = re.sub('\s+', '', fix_line)
        for pred in preds:
            pred = re.sub('\s+', '', pred)
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
        try:
            fix_line = get_tokens(fix_line)
        except Exception as e:
            return False
        fix_line = ''.join(fix_line)
        for pred in preds:
            temp = pred

            pred = re.sub('\s+', ' ', pred)
            try:
                pred = get_tokens(pred)
            except Exception as e:
                continue
            pred = restore(pred, rep, raw)
            pred = ''.join(pred)
            if pred == fix_line:
                return True

    if model == 'AddCast':
        fix_line = re.sub('\s+', '', fix_line)
        for pred in preds:
            pred = re.sub('\s+', '', pred)
            rep = re.sub('\s+', '', rep)
            pred.replace(rep, raw)
            if pred == fix_line:
                return True

    return False


if __name__ == '__main__':
    ids_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\patches\sequenceR.sids'
    input_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\patches\sequenceR.buggy'
    pred_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\patches\sequenceR_diversity.pred'

    changes_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\changes'
    fix_lines_path = r'F:\workspace\bug_detection\data\Dataset\fixed_lines'
    #buggy_methods_path = r'F:\workspace\bug_detection\data\Dataset\buggy_methods'

    preds = read_files(pred_path)
    #inputs = read_files(input_path)
    ids = read_files(ids_path)

    count = 0
    id_dir = {}
    for i, id_with_trans in enumerate(ids):
        infos = id_with_trans.split('---')
        idx = infos[0]

        if not idx in id_dir:
            id_dir[idx] = {}

        fix_line = os.path.join(fix_lines_path, f'{idx}.txt')
        with open(fix_line, encoding='utf-8') as fp:
            fix_line = fp.read().strip()

        success = None
        if len(infos) == 1:
            success = fix_test(fix_line, preds[i * 100: (i + 1) * 100])
        else:
            change_path = os.path.join(changes_path, f'{id_with_trans}.txt')
            with open(change_path, encoding='utf-8') as fp:
                change = fp.read()
            change = change.split('->')
            success = fix_test(fix_line, preds[i * 100: (i + 1) * 100], model=infos[1], raw=change[0], rep=change[1])

        id_dir[idx][id_with_trans] = success

        if i % 1000 == 0:
            print(f'{i} / {len(ids)}')
    with open('temp.json', 'w', encoding='utf-8') as fp:
        json.dump(id_dir, fp, ensure_ascii=False, indent=4)



# fix_line = os.path.join(fix_lines_path, f'{idx}.txt')
# with open(fix_line, encoding='utf-8') as fp:
#     fix_line = fp.read().strip()
# success = fix_test(fix_line, preds[i * 100: (i + 1) * 100])

