import re
import json
import os
from tqdm import tqdm
import datetime
from javalang import tokenizer

def remove_comments(method: str):
    lines = method.split('\n')
    lines = [line for line in lines if not line.strip().startswith('//')]
    return ''.join(lines)

def read_files(path):
    with open(path, encoding='utf-8') as fp:
        data = fp.readlines()
    data = [line.strip() for line in data]
    return data


def replace_abs(map_path, code):
    with open(map_path, encoding='utf-8') as fp:
        try:
            data = json.load(fp)
        except Exception as e:
            return None

    for key, value in data.items():
        code = code.replace(value, key)

    return code


def fix_test(fix_method, preds, map_path, model='raw', raw=None, rep=None):
    assert model in ['raw', 'ChangeName', 'AddCast']
    if model == 'raw':
        fix_method = re.sub('\s+', '', fix_method)
        for pred in preds:
            pred = replace_abs(map_path, pred)
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

        # try:
        #     fix_method = get_tokens(fix_method)
        # except Exception as e:
        #     return False
        fix_method = re.sub('\s+', '', fix_method)
        for pred in preds:
            pred = replace_abs(map_path, pred)
            # try:
            #     pred = get_tokens(pred)
            # except Exception as e:
            #     continue
            #tufano输出时直接输出以空格为间隔的token，所以直接split即可
            pred = pred.split()
            pred = restore(pred, rep, raw)
            pred = ''.join(pred)
            pred = re.sub('\s+', '', pred)
            if pred == fix_method:
                return True

    if model == 'AddCast':
        fix_method = re.sub('\s+', '', fix_method)
        for pred in preds:
            pred = replace_abs(map_path, pred)
            pred = re.sub('\s+', '', pred)
            rep = re.sub('\s+', '', rep)
            pred = pred.replace(rep, raw)
            if pred == fix_method:
                return True

    return False

def fix_test1(fix_method, preds, map_path, model='raw', raw=None, rep=None):
    assert model in ['raw', 'ChangeName', 'AddCast']
    if model == 'raw':
        fix_method = remove_comments(fix_method)
        fix_method = re.sub('\s+', '', fix_method)
        for pred in preds:
            pred = replace_abs(map_path, pred)
            pred = re.sub('\s+', '', pred)
            if pred == fix_method:
                return True

    if model == 'ChangeName':

        def restore(tokens, raw, rep):
            for i, token in enumerate(tokens):
                if token == raw:
                    tokens[i] = rep
            return tokens

        # try:
        #     fix_method = get_tokens(fix_method)
        # except Exception as e:
        #     return False
        fix_method = remove_comments(fix_method)
        fix_method = re.sub('\s+', '', fix_method)
        for pred in preds:
            pred = replace_abs(map_path, pred)
            # try:
            #     pred = get_tokens(pred)
            # except Exception as e:
            #     continue
            #tufano输出时直接输出以空格为间隔的token，所以直接split即可
            pred = pred.split()
            pred = restore(pred, rep, raw)
            pred = ''.join(pred)
            pred = re.sub('\s+', '', pred)
            if pred == fix_method:
                return True

    if model == 'AddCast':
        fix_method = remove_comments(fix_method)
        fix_method = re.sub('\s+', '', fix_method)
        for pred in preds:
            pred = replace_abs(map_path, pred)
            pred = re.sub('\s+', '', pred)
            rep = re.sub('\s+', '', rep)
            pred = pred.replace(rep, raw)
            if pred == fix_method:
                return True

    return False

def read_fix_method(path):
    #去除第一行的注解
    with open(path, encoding='utf-8') as fp:
        lines = fp.readlines()

    lines[0] = lines[0].lstrip()
    if lines[0].startswith('@'):
        lines = lines[1: ]

    return "".join(lines)



def main():
    preds_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\patches\Tufano_diversity.pred'
    ids_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\patches\Tufano.sids'
    maps_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\patches\temps_tufano'

    changes_path = r'F:\workspace\bug_detection\data\Dataset\diversity_data\changes'
    fix_methods_path = r'F:\workspace\bug_detection\data\Dataset\fixed_methods'

    preds = read_files(preds_path)
    ids = read_files(ids_path)

    count = 0
    id_dir = {}
    for i, id_with_trans in enumerate(ids):
        infos = id_with_trans.split('---')
        idx = infos[0]

        if not idx in id_dir:
            id_dir[idx] = {}

        fix_method = os.path.join(fix_methods_path, f'{idx}.txt')
        fix_method = read_fix_method(fix_method)

        success = None
        map_path = os.path.join(maps_path, f'{id_with_trans}_buggy.txt.abs.map')
        if len(infos) == 1:
            success = fix_test1(fix_method, preds[i * 100: (i + 1) * 100], map_path)
        else:
            change_path = os.path.join(changes_path, f'{id_with_trans}.txt')
            with open(change_path, encoding='utf-8') as fp:
                change = fp.read()
            change = change.split('->')
            success = fix_test1(fix_method, preds[i * 100: (i + 1) * 100], map_path, model=infos[1], raw=change[0], rep=change[1])

        id_dir[idx][id_with_trans] = success
        if success:
            count += 1
        if i % 100 == 0:
            print(f'{i} / {len(ids)}, count: {count}')

    with open(f'tufano_result_{datetime.date.today()}_no_comment.json', 'w', encoding='utf-8') as fp:
        json.dump(id_dir, fp, ensure_ascii=False, indent=4)




main()