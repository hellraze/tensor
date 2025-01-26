import git
import os
import shutil
import datetime
import glob
import json
from git import exc

def clone_repo(repo_url):
    url_parts = repo_url.split('/')
    dir_name = url_parts[-1]

    local_dir = f'../repos/{dir_name}'

    try:
        git.Repo.clone_from(repo_url, local_dir)
        time = datetime.datetime.now()
        print(time, end=": ")
        print(f'Репозиторий успешно склонирован: {"/".join(local_dir.split("/")[1:])}')
        return local_dir
    except exc.GitCommandError as e:
        print(f'Exception: {e}')


def rm_others(parent_dir, target_dir):
    for folder_name in os.listdir(parent_dir):
        folder_path = os.path.join(parent_dir, folder_name)

        if os.path.isdir(folder_path) and folder_name != target_dir:
            if not folder_name.startswith('.'):
                shutil.rmtree(folder_path)
                time = datetime.datetime.now()
                print(time, end=": ")
                print(f'Папка {folder_path} удалена')

def rm_except_target(parent_dir,target_dir):
    dirs = target_dir.split("/")

    for dir in dirs:
        rm_others(parent_dir, dir)
        parent_dir += f'/{dir}'


def archive_folder(folder_path, archive_name, output_dir):
    full_archive_name = os.path.join(output_dir, archive_name)

    shutil.make_archive(full_archive_name, 'zip', folder_path)

    time = datetime.datetime.now()
    print(time, end=": ")
    print(f"Архив {full_archive_name}.zip успешно создан.")

def make_json(folder_path, version):
    file_extensions = ['*.py', '*.js', '*.sh']
    files = []

    for extension in file_extensions:
        search_pattern = os.path.join(folder_path, extension)
        files.extend(glob.glob(search_pattern))

    for file in files:
        time = datetime.datetime.now()
        print(time, end=": ")
        print("Найден файл:", file)

    files_for_json = []

    for file in files:
        files_for_json.append(file.split('\\')[1])

    data = {
        'name': 'hello world',
        'version': version,
        'files': files_for_json
    }

    json_file = os.path.join(folder_path, 'version.json')
    json_string = json.dumps(data, indent=4)
    with open(json_file, 'w') as f:
        f.write(json_string)

    time = datetime.datetime.now()
    print(time, end=": ")
    print(f'Файл {json_file} успешно создан и сохранен.')




if __name__ == "__main__":
    url = input("Введите адрес репозитория: ")

    target_dir = input("Введите относительный путь внутри репозитория до исходного кода: ")
    local_dir = clone_repo(url)

    today = datetime.date.today()
    today_str = today.strftime('%d%m%Y')

    rm_except_target(local_dir, target_dir)

    version = input("Введите версию будущего продукта: ")
    make_json(local_dir + '/' + target_dir, version)

    archive_name = target_dir.split("/")[-1] + today_str
    output_dir = '../repos/archives'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    archive_folder(local_dir, archive_name, output_dir)

