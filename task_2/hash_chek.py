import hashlib
import os
import sys


def hash_file_to_list(file_path):
    """Функция считывания файла с hash."""
    res = []
    if not os.path.exists(file_path):
        print('hash file not found')
        return res

    with open(file_path, 'r') as file:
        for line in file:
            line = line.rstrip('\n').split()
            res.append(line)
    return res


def check_file_hash(file, hash_obj, hash_sum):
    """Функция проверки hash файла."""
    data = file.read(2048)
    hash_obj.update(data)
    if hash_sum == hash_obj.hexdigest():
        return 'OK'
    return 'FAIL'


def open_files_to_check(file_list, directory):
    """Функция открытия и проверки файлов."""
    for item in file_list:
        file_name = item[0]
        alg = item[1]
        hash_sum = item[2]
        file_path = f'{directory}/{file_name}'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                if alg == 'md5':
                    status = check_file_hash(file, hashlib.md5(), hash_sum)
                elif alg == 'sha1':
                    status = check_file_hash(file, hashlib.sha1(), hash_sum)
                elif alg == 'sha256':
                    status = check_file_hash(file, hashlib.sha256(), hash_sum)
                elif alg == 'sha384':
                    status = check_file_hash(file, hashlib.sha384(), hash_sum)
                else:
                    status = f'Unexpected algorithm {alg}, file {file.name}'
        else:
            status = 'Not found'
        print(file_name, status)


def main():
    hash_file_path = sys.argv[1]
    files_path = sys.argv[2]
    file_list = hash_file_to_list(hash_file_path)
    open_files_to_check(file_list, files_path)


if __name__ == '__main__':
    main()
