import os
import json
import datetime
import re
from javalang import tokenizer

def read_lines(path):
    with open(path, encoding='utf-8') as fp:
        lines = fp.readlines()
    return [line.strip() for line in lines]


def my_read(path):
    with open(path, encoding='utf-8') as fp:
        return fp.read()

def my_read_json(path):
    with open(path, encoding='utf-8') as fp:
        return json.load(fp)



def fix_test(fix_method, preds, model = 'raw', raw=None, rep=None):
    assert model in ['raw', 'ChangeName', 'AddCast']
    fix_method = re.sub('\s+', '', fix_method)
    if model == 'raw':
        for _, pred in preds.items():
            pred = re.sub('\s+', '', pred)
            if pred == fix_method:
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
        for _, pred in preds.items():
            try:
                pred = get_tokens(pred)
            except Exception as e:
                continue
            pred = restore(pred, rep, raw)
            pred = ''.join(pred)
            pred = re.sub('\s+', '', pred)
            if pred == fix_method:
                return True

    if model == 'AddCast':
        for _, pred in preds.items():
            pred = re.sub('\s+', '', pred)
            rep = re.sub('\s+', '', rep)
            pred = pred.replace(rep, raw)
            if pred == fix_method:
                return True

    return False



def main():
    pred_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\patches\new_outputs_recoder'

    changes_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\changes'
    fix_methods_path = r'F:\workspace\bug_detection\data\Dataset\fixed_methods'

    pred_files = os.listdir(pred_path)
    ids = [file.replace(".fix", "") for file in pred_files]
    id_dir = {}

    count = 0
    fail_count = 0
    for i, id_with_trans in enumerate(ids):
        infos = id_with_trans.split('---')
        idx = infos[0]

        if not idx in id_dir:
            id_dir[idx] = {}

        fix_method = os.path.join(fix_methods_path, f'{idx}.txt')
        fix_method = my_read(fix_method)
        pred = os.path.join(pred_path, f'{id_with_trans}.fix')
        try:
            pred = my_read_json(pred)
        except Exception as e:
            print(e)
            print(id_with_trans)
            fail_count += 1
            continue

        success = None

        if len(infos) == 1:
            success = fix_test(fix_method, pred)
        else:
            change = os.path.join(changes_path, f'{id_with_trans}.txt')
            change = my_read(change)
            change = change.split('->')
            success = fix_test(fix_method, pred, model=infos[1], raw=change[0], rep = change[1])


        id_dir[idx][id_with_trans] = success

        if success:
            count += 1
        if i % 100 == 0:
            print(f'{i} / {len(ids)}, count: {count}')

    with open(f'./result/recoder_result_{datetime.date.today()}.json', 'w', encoding='utf-8') as fp:
        json.dump(id_dir, fp, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()

