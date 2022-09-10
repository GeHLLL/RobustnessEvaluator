import os
import shutil
import yaml
import subprocess
import argparse

from datetime import date

import utils


def d4j_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str)
    args = parser.parse_args()

    config_path = args.config
    with open(config_path, encoding='utf-8') as fp:
        config = yaml.load(fp, yaml.FullLoader)

    patches_path = os.path.join(config['patches_path'], f'{config["model_name"]}.patches')
    infos_path = './config/infos.json'
    result_path = os.path.join(config['result_path'], f'{config["model_name"]}-{date.today()}.json')

    patches = utils.my_json_load(patches_path)
    infos: dict = utils.my_json_load(infos_path)

    curr_path = os.path.abspath('./')

    result = {}

    for _, value in infos.items():
        ids = value['id_with_trans']
        bug_name = value['bug_name']
        raw_buggy_path = os.path.join(config['raw_d4j_path'], f'{bug_name}_buggy')
        new_buggy_path = os.path.join(config['d4j_path'], f'{bug_name}_buggy')
        java_path = config['d4j_path'] + value['java_path']
        print(f'start to test {bug_name}')

        for idx in ids:
            if idx not in patches:
                continue

            idx_data = {}
            idx_data['compile_success'] = False
            idx_data['test_success'] = False
            idx_data['fail_infos'] = []

            if os.path.exists(new_buggy_path):
                shutil.rmtree(new_buggy_path)
            shutil.copytree(raw_buggy_path, new_buggy_path)
            os.remove(java_path)
            with open(java_path, 'w', encoding='utf-8') as fp:
                fp.write(patches[idx])

            os.chdir(new_buggy_path)

            # compile_info = os.popen(f'timeout {config["timeout"]} mvn compile')
            # compile_info = compile_info.read()
            # if 'BUILD SUCCESS' in compile_info:

            compile_info = subprocess.Popen(['timeout', config['timeout'], 'defects4j', 'compile'],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
            _, compile_info = compile_info.communicate()
            compile_info = str(compile_info, 'utf-8').strip().split('\n')
            if utils.D4j_utils.compile_success(compile_info):
                idx_data['compile_success'] = True

                # test_info = os.popen(f'timeout {config["timeout"]} mvn test -e')
                # test_info = test_info.read()
                # test_info = test_info.split('Results :')[-1]
                # if 'Failures: 0' in test_info and 'Errors: 0' in test_info:

                test_info = subprocess.Popen(['timeout', config['timeout'], 'defects4j', 'test'],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                test_info, _ = test_info.communicate()
                test_info = str(test_info, 'utf-8').strip().split('\n')
                if utils.D4j_utils.test_success(test_info):
                    idx_data['test_success'] = True
                else:
                    # reports_path = os.path.join(new_buggy_path, 'target', 'surefire-reports')
                    # reports = [file for file in os.listdir(reports_path) if file.endswith('.txt')]
                    # for file in reports:
                    #     report_path = os.path.join(reports_path, file)
                    #     report = utils.my_read(report_path)
                    #     if '<<< FAILURE!' in report:
                    #         idx_data['fail_infos'].append(report)

                    failing_tests_path = os.path.join(new_buggy_path, 'failing_tests')
                    failing_tests = utils.my_read(failing_tests_path)
                    idx_data['fail_infos'].append(failing_tests)



            result.update({idx: idx_data})
            os.chdir(curr_path)



    utils.my_json_dump(result, result_path)





if __name__ == '__main__':
    d4j_main()




