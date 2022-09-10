import os
import json
import re
import utils
import csv

def remove_java_line_info(str, value):
    java_name = value['java_path'].split('/')[-1]
    regex = f'\({java_name}:[0-9]+\)'
    str = re.sub(regex, '', json.dumps(str))
    return str


def check(model):
    info_path = './config/infos.json'
    results_path = r'F:\workspace\bug_detection\data\Dataset_d4j\trans_d4j\result\results\results'
    raw_result_path = os.path.join(results_path, f'{model}_raw.json')
    trans_result_path = os.path.join(results_path, f'{model}_trans.json')

    info = utils.my_json_load(info_path)
    raw_result = utils.my_json_load(raw_result_path)
    trans_result = utils.my_json_load(trans_result_path)

    trans_types = ['ChangeName', 'AddCast', 'UnusedStatement', 'NewVariable']

    count = 0
    trans_count = 0
    result_dic = {}
    result_dic['Total'] = {'fail': 0, 'fail_count': 0, 'all': 0}
    for t in trans_types:
        result_dic[t] = {'fail': 0, 'fail_count': 0, 'all': 0}


    for bug, value in info.items():
        if not bug in raw_result:
            continue

        count += 1

        raw_info = raw_result[bug]
        raw_info = remove_java_line_info(json.dumps(raw_info), value)

        id_with_trans = value['id_with_trans']

        exist_fail = False
        exist_type_fail = [False] * len(trans_types)
        for idx in id_with_trans:
            if not idx in trans_result:
                continue



            idx_info = idx.split('---')
            idx_type = idx_info[-2]

            trans_count += 1
            result_dic['Total']['all'] = result_dic['Total']['all'] + 1
            result_dic[idx_type]['all'] = result_dic[idx_type]['all'] + 1

            trans_info = trans_result[idx]
            trans_info = remove_java_line_info(json.dumps(trans_info), value)

            if not trans_info == raw_info:
                if r'{\"compile_success\": true,' in trans_info and r'{\"compile_success\": true,' in raw_info:
                    print(idx)
                    print('-'*89)
                    print(raw_info)
                    print('-' *89)
                    print(trans_info)
                    print('-'*89)
                exist_fail = True
                result_dic['Total']['fail_count'] = result_dic['Total']['fail_count'] + 1
                exist_type_fail[trans_types.index(idx_type)] = True
                result_dic[idx_type]['fail_count'] = result_dic[idx_type]['fail_count'] + 1

        if exist_fail:
            result_dic['Total']['fail'] = result_dic['Total']['fail'] + 1

        for t in trans_types:
            if exist_type_fail[trans_types.index(t)]:
                result_dic[t]['fail'] = result_dic[t]['fail'] + 1

    return count, result_dic


def new_check(model):
    results_path = './filter3_results'
    result = utils.my_json_load(os.path.join(results_path, f'{model}_result.json'))

    trans_types = ['ChangeName', 'AddCast', 'UnusedStatement', 'NewVariable']

    result_dic = {}
    result_dic['Total'] = {'fail': 0, 'fail_count': 0}

    for t in trans_types:
        result_dic[t] = {'fail': 0, 'fail_count': 0}

    for bug, value in result.items():
        exist_fail = False
        exist_type_fail = [False] * len(trans_types)

        for idx in value:
            idx_info = idx.split('---')
            idx_type = idx_info[-2]

            if not value[idx]:
                exist_fail = True
                exist_type_fail[trans_types.index(idx_type)] = True
                result_dic['Total']['fail_count'] = result_dic['Total']['fail_count'] + 1
                result_dic[idx_type]['fail_count'] = result_dic[idx_type]['fail_count'] + 1

        if exist_fail:
            result_dic['Total']['fail'] = result_dic['Total']['fail'] + 1

        for t in trans_types:
            if exist_type_fail[trans_types.index(t)]:
                result_dic[t]['fail'] = result_dic[t]['fail'] + 1

    return result_dic


if __name__ == '__main__':
    path = r'filter3_results'
    files = os.listdir(path)
    files = [file.replace('_result.json', '')for file in files]
    models = list(set(files))
    models.sort()
    print(models)

    operations = ['VR', 'UC', 'UV', 'NV']
    list1 = [o +' Fail' for o in operations]
    list2 =  ['Fail after ' +o for o in operations]
    fp = open('result5.csv', 'w', newline='')
    myWriter = csv.writer(fp)
    myWriter.writerow(['', ] + list1 + list2 + ['Fail after trans'])

    for model in models:
        line = []
        line.append(model)
        print(f'start to check {model}')
        result = new_check(model)

        print(result)

        line.append(f'{result["ChangeName"]["fail_count"]}')

        line.append(f'{result["AddCast"]["fail_count"]}')
        line.append(f'{result["UnusedStatement"]["fail_count"]}')
        line.append(f'{result["NewVariable"]["fail_count"]}')

        line.append(f"{result['ChangeName']['fail']}")
        line.append(f"{result['AddCast']['fail']}")
        line.append(f"{result['UnusedStatement']['fail']}")
        line.append(f"{result['NewVariable']['fail']}")
        line.append(f"{result['Total']['fail']}")


        myWriter.writerow(line)

    fp.close()



