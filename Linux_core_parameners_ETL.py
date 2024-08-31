import requests
import re
import oracledb

USER = ''
PASSWORD = ''
DSN = ''


def get_sql_scripts(connection):
    sqls = {}
    with connection.cursor() as cursor:
        for r in cursor.execute("SELECT s.CODE, s.SCRIPT "
                                "FROM APP_APEX_MICROSERVICES.V_PYTHON_SQL s "
                                "WHERE s.PROJECT_NAME = 'load_linux_core_parameters_info' "
                                "ORDER BY s.ID "):
            sqls[str(r[0])] = ''.join(r[1].read())
    return sqls


def _get_abi():
    params = ['abi']
    url = 'https://www.kernel.org/doc/Documentation/sysctl/'

    for param_prefix in params:
        req = requests.get(url + param_prefix + '.txt')

        params_arr = req.text.split('===========================================================')
        params_arr.pop(0)
        params_arr.pop(0)
        params_arr.pop(len(params_arr) - 1)

        params_dict = {param_prefix+'.'+a.strip().split('\n')[0].strip(':'): '\n'.join(a.strip().split('\n')[1:])
                       for a in params_arr}

        with oracledb.connect(user=USER,
                              password=PASSWORD,
                              dsn=DSN) as connection_apex:
            sql_list = get_sql_scripts(connection_apex)
            with connection_apex.cursor() as cursor_apex:
                for key in params_dict:
                    cursor_apex.execute(sql_list['LOAD_LINUX_CORE_PARAMETERS_INFO_MERGE'],
                                        param=key,
                                        description=params_dict[key].strip())

                connection_apex.commit()


def _get_fs():
    params = ['fs']
    url = 'https://www.kernel.org/doc/Documentation/sysctl/'

    for param_prefix in params:
        req = requests.get(url + param_prefix + '.txt')

        params_arr = req.text.split('==============================================================')

        params_arr.pop(0)
        params_arr.pop(0)
        params_arr.pop(len(params_arr) - 1)

        params_dict_temp = {}
        for params in params_arr:
            param = params.strip().split('\n')[0].strip(':')
            if param in params_dict_temp:
                params_dict_temp[param] = params_dict_temp[param] + '\n'+'\n'.join(params.strip().split('\n')[1:])
            else:
                params_dict_temp[param] = '\n'.join(params.strip().split('\n')[1:])

        params_dict = {}

        for key in params_dict_temp:
            key_tmp = key.split(':')[0]
            keys_tmp = re.split(r'[&,]+|and ', key_tmp)
            for key_tmp in keys_tmp:
                if key_tmp.strip() != '':
                    param = param_prefix + '.' + key_tmp.strip()
                    params_dict[param] = params_dict_temp[key].strip()

        with oracledb.connect(user=USER,
                              password=PASSWORD,
                              dsn=DSN) as connection_apex:
            sql_list = get_sql_scripts(connection_apex)
            with connection_apex.cursor() as cursor_apex:
                for key in params_dict:
                    cursor_apex.execute(sql_list['LOAD_LINUX_CORE_PARAMETERS_INFO_MERGE'],
                                        param=key,
                                        description=params_dict[key])

                connection_apex.commit()


def _get_kernel():
    params = ['kernel']
    url = 'https://www.kernel.org/doc/Documentation/sysctl/'

    for param_prefix in params:
        req = requests.get(url + param_prefix + '.txt')

        params_arr = req.text.split('==============================================================')

        params_arr.pop(0)
        params_arr.pop(0)
        params_arr.pop(len(params_arr) - 1)

        params_dict_temp = {a.strip().split('\n')[0].strip(':'): '\n'.join(a.strip().split('\n')[1:])
                            for a in params_arr}

        params_dict = {}

        for key in params_dict_temp:
            key_tmp = key.split(':')[0]
            keys_tmp = re.split(r'[&,]+|and ', key_tmp)
            for key_tmp in keys_tmp:
                if key_tmp.strip() != '':
                    params_dict[param_prefix + '.' + key_tmp.strip()] = params_dict_temp[key].strip()

        with oracledb.connect(user=USER,
                              password=PASSWORD,
                              dsn=DSN) as connection_apex:
            sql_list = get_sql_scripts(connection_apex)
            with connection_apex.cursor() as cursor_apex:
                for key in params_dict:
                    cursor_apex.execute(sql_list['LOAD_LINUX_CORE_PARAMETERS_INFO_MERGE'],
                                        param=key,
                                        description=params_dict[key])

                connection_apex.commit()


def _get_net_core():
    params = ['net']
    url = 'https://www.kernel.org/doc/Documentation/sysctl/'

    for param_prefix in params:
        req = requests.get(url + param_prefix + '.txt')

        params_arr = req.text.split('-------------------------------------------------------')
        net_core = params_arr[1]
        net_core = net_core.replace('------------------------------', '&&&')
        net_core = net_core.replace('----------------------------', '&&&')
        net_core = net_core.replace('----------------------', '&&&')
        net_core = net_core.replace('---------------------', '&&&')
        net_core = net_core.replace('------------------', '&&&')
        net_core = net_core.replace('----------------', '&&&')
        net_core = net_core.replace('--------------', '&&&')
        net_core = net_core.replace('-------------', '&&&')
        net_core = net_core.replace('------------', '&&&')
        net_core = net_core.replace('----------', '&&&')
        net_core = net_core.replace('--------', '&&&')
        net_core_params_arr = net_core.split('&&&')
        params_dict_temp = {}
        params_dict = {}

        for i in range(len(net_core_params_arr)):
            if i != 0:
                param = net_core_params_arr[i - 1].strip().split('\n')[-1].strip()
                value = '\n'.join(net_core_params_arr[i].split('\n')[:-2]).strip()
                params_dict_temp[param] = value

        for key in params_dict_temp:
            key_tmp = key.split(':')[0]
            keys_tmp = re.split(r'[&,]+|and ', key_tmp)
            for key_tmp in keys_tmp:
                if key_tmp.strip() != '':
                    params_dict[param_prefix + '.core.' + key_tmp.strip()] = params_dict_temp[key].strip('-').strip()

        with oracledb.connect(user=USER,
                              password=PASSWORD,
                              dsn=DSN) as connection_apex:
            sql_list = get_sql_scripts(connection_apex)
            with connection_apex.cursor() as cursor_apex:
                for key in params_dict:
                    cursor_apex.execute(sql_list['LOAD_LINUX_CORE_PARAMETERS_INFO_MERGE'],
                                        param=key,
                                        description=params_dict[key])

                connection_apex.commit()


def _get_net_tipc():
    params = ['net']
    url = 'https://www.kernel.org/doc/Documentation/sysctl/'

    for param_prefix in params:
        req = requests.get(url + param_prefix + '.txt')

        params_arr = req.text.split('-------------------------------------------------------')
        net_tipc = params_arr[6]
        net_tipc = net_tipc.replace('--------------', '&&&')
        net_tipc = net_tipc.replace('----------', '&&&')

        net_core_params_arr = net_tipc.split('&&&')
        params_dict_temp = {}
        params_dict = {}

        for i in range(len(net_core_params_arr)):
            if i != 0:
                param = net_core_params_arr[i - 1].strip().split('\n')[-1].strip()
                value = '\n'.join(net_core_params_arr[i].split('\n')[:-2]).strip()
                params_dict_temp[param] = value

        for key in params_dict_temp:
            key_tmp = key.split(':')[0]
            keys_tmp = re.split(r'[&,]+|and ', key_tmp)
            for key_tmp in keys_tmp:
                if key_tmp.strip() != '':
                    params_dict[param_prefix + '.tipc.' + key_tmp.strip()] = params_dict_temp[key].strip('-').strip()

        with oracledb.connect(user=USER,
                              password=PASSWORD,
                              dsn=DSN) as connection_apex:
            sql_list = get_sql_scripts(connection_apex)
            with connection_apex.cursor() as cursor_apex:
                for key in params_dict:
                    cursor_apex.execute(sql_list['LOAD_LINUX_CORE_PARAMETERS_INFO_MERGE'],
                                        param=key,
                                        description=params_dict[key])

                connection_apex.commit()


def _get_user():
    params = ['user']
    url = 'https://www.kernel.org/doc/Documentation/sysctl/'

    for param_prefix in params:
        req = requests.get(url + param_prefix + '.txt')

        params_arr = req.text.split('- ')
        params_arr.pop(0)

        params_dict = {param_prefix + '.' + a.strip().split('\n')[0].strip(): '\n'.join(a.strip().split('\n')[1:])
                       for a in params_arr}

        print(params_dict)

        with oracledb.connect(user=USER,
                              password=PASSWORD,
                              dsn=DSN) as connection_apex:
            sql_list = get_sql_scripts(connection_apex)
            with connection_apex.cursor() as cursor_apex:
                for key in params_dict:
                    cursor_apex.execute(sql_list['LOAD_LINUX_CORE_PARAMETERS_INFO_MERGE'],
                                        param=key,
                                        description=params_dict[key].strip())

                connection_apex.commit()


def _get_vm():
    params = ['vm']
    url = 'https://www.kernel.org/doc/Documentation/sysctl/'

    for param_prefix in params:
        req = requests.get(url + param_prefix + '.txt')

        vm = req.text
        vm = vm.replace('==============================================================', '&&&')
        vm = vm.replace('=============================================================', '&&&')

        vm = (vm.replace('------------------', '')
              .replace('============ End of Document =================================', ''))

        params_arr = vm.split('&&&')

        params_arr.pop(0)
        params_arr.pop(0)

        params_dict_temp = {a.strip().split('\n')[0].strip(':'): '\n'.join(a.strip().split('\n')[1:])
                            for a in params_arr}

        params_dict = {}

        for key in params_dict_temp:
            key_tmp = key.split(':')[0]
            keys_tmp = re.split(r'[&,]+|and ', key_tmp)
            for key_tmp in keys_tmp:
                if key_tmp.strip() != '':
                    params_dict[param_prefix + '.' + key_tmp.strip()] = params_dict_temp[key].strip()

        with oracledb.connect(user=USER,
                              password=PASSWORD,
                              dsn=DSN) as connection_apex:
            sql_list = get_sql_scripts(connection_apex)
            with connection_apex.cursor() as cursor_apex:
                for key in params_dict:
                    cursor_apex.execute(sql_list['LOAD_LINUX_CORE_PARAMETERS_INFO_MERGE'],
                                        param=key,
                                        description=params_dict[key])

                connection_apex.commit()



_get_abi()
_get_fs()
_get_kernel()
_get_net_core()
_get_net_tipc()
_get_user()
_get_vm()