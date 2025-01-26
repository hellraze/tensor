import json
import itertools


def generate_versions(template):
    parts = template.split('.')

    options = []
    for part in parts:
        if part == '*':
            options.append(['0', '1', '2'])
        else:
            options.append([part])

    all_combinations = itertools.product(*options)

    versions = ['.'.join(combination) for combination in all_combinations]
    return versions


def main(version_input, filename):
    config = get_data_from_json(filename)

    all_versions = []
    for template in config.values():
        all_versions.extend(generate_versions(template))

    all_versions_sorted = sorted(set(all_versions))

    print("Отсортированные версии:")
    for version in all_versions_sorted:
        print(version)

    version_input_parts = version_input.split('.')

    print("\nВерсии, меньшие чем введенная версия:")
    for version in all_versions_sorted:
        version_parts = version.split('.')

        if version_parts < version_input_parts:
            print(version)


def get_data_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    return data

if __name__ == "__main__":
    input_version = input('Введите версию: ')
    config_file = input('Введите расположение и имя файла: ')

    main(input_version, config_file)