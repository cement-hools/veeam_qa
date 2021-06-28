import os
import shutil
import xml.dom.minidom


def copy_files(conf_list):
    """Копирование файлов согласно настройкам."""
    for file in conf_list:
        source_path = file.getAttribute('source_path') or None
        destination_path = file.getAttribute('destination_path') or None
        file_name = file.getAttribute('file_name') or None
        if not (source_path and destination_path and file_name):
            continue
        file_exists = os.path.exists(f'{source_path}/{file_name}')
        destination_path_exists = os.path.exists(destination_path)
        if file_exists:
            if not destination_path_exists:
                os.mkdir(destination_path)
            shutil.copy(f'{source_path}/{file_name}', f'{destination_path}')
            print(f'file {source_path}/{file_name} copy to {destination_path}')
        else:
            print(f'file {source_path}/{file_name} not exists')


def main():
    dom = xml.dom.minidom.parse('conf.xml')
    dom.normalize()

    conf_list = dom.getElementsByTagName('file')

    copy_files(conf_list)


if __name__ == '__main__':
    main()
