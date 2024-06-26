import os
import re
import json


# get the daily problem name and date
problems = {}


def read_data():
    # read the data from the file
    with open('.github/data/problems.json', 'r') as file:
        data = json.loads(file.read())

    # return the data
    return data


def change_directory(dir=None, monthly=None, daily=None):
    if daily is not None and monthly is not None and dir is not None:
        os.chdir(f"{dir}/{monthly}/{daily}")
    elif monthly is not None and dir is not None:
        os.chdir(f"{dir}/{monthly}")
    elif dir is not None:
        os.chdir(f"{dir}")


def check_monthly_folders():

    # name of the folders in the directory
    folders = [f for f in os.listdir(".") if os.path.isdir(f)]

    # delete .github from them
    folders.remove(".github")
    folders.remove(".git")

    # check if the folders are in the directory
    for folder in folders:
        if folder not in problems:
            print(f"Folder {folder} name is not valid")
            exit(1)

    # if the folders is valid
    return folders


def check_daily_folders(monthly_folder):

    # name of the folders in the directory
    folders = [f for f in os.listdir() if os.path.isdir(f)]

    # daily problems folders
    problems_folders = problems[monthly_folder]

    # check if the folders are in the directory
    for folder in folders:

        # make sure the folder is in the problems
        parts = folder.split(' ')
        parts[0] = parts[0][:-1]

        problem = {
            "day": parts[0],
            "title": ' '.join(parts[1:])
        }

        if problem not in problems_folders:
            print(f"Folder {folder} name is not valid")
            exit(1)

    # if the folders is valid
    return folders


def check_files(folder_name):

    # name of the folders in the directory
    files = [f for f in os.listdir() if os.path.isfile(f)]

    # check if the folders are in the directory
    for file in files:
        user_with_ext = file.replace(folder_name, '')
        if not re.match(
            r"([A-Za-z -_]+).[cpp|rb|py|js|ts|c|java|php|dart]",
            user_with_ext,
        ) or not user_with_ext[0].isspace():
            print(f"file {file} name is not valid")
            exit(1)


def main():
    # read the global problems
    global problems

    # read the problems from the data file
    problems = read_data()

    # check folders in the repo
    monthly_folders = check_monthly_folders()

    # directory of the root folder
    dir = os.getcwd()

    # check folders in the monthly folders
    for monthly_folder in monthly_folders:
        # change directory to the current monthly folder
        change_directory(monthly=monthly_folder, dir=dir)

        # check folders in the monthly folder
        daily_folders = check_daily_folders(monthly_folder)

        for daily_folder in daily_folders:

            # change directory to the current daily folder
            change_directory(daily=daily_folder, monthly=monthly_folder, dir=dir)

            # check files in the daily folder
            check_files(daily_folder)

            # change directory to the monthly folder again
            change_directory(monthly=monthly_folder, dir=dir)

        # change directory to the main folder again
        change_directory(dir=dir)

    print("All files are valid")


if __name__ == "__main__":
    main()
