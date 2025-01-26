import git
import os
import shutil
import datetime
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


if __name__ == "__main__":
    url = 'https://github.com/paulbouwer/hello-kubernetes'
    target_dir = "src/app"
    local_dir = clone_repo(url)

    today = datetime.date.today()

    today_str = today.strftime('%d%m%Y')

    archive_name = target_dir.split("/")[-1] + today_str

    rm_except_target(local_dir, target_dir)

    output_dir = '../repos/archives'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    archive_folder(local_dir, archive_name, output_dir)
