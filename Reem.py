from datetime import date
from datetime import datetime
import base64
from github import Github
from github import InputGitTreeElement
from airium import Airium
def login():
    print("########################")
    print("TIME:", datetime.now())
    print("########################")
    print("Water Maintenance System")
    print("########################")
    global username
    global password
    username = input("Enter your username:\n")
    password = input("Enter your password:\n")

def pushhub(data):
    git = Github("")
    repo = git.get_user().get_repo('watermaintain')
    file_list = ['C://Users//Administrator//Desktop//Project//index.html']
    file_names = ['index.html']
    commit_message = "Schedule for {}".format(datetime.now())
    master_ref = repo.get_git_ref('heads/main')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    element_list = list()
    for i, entry in enumerate(file_list):
        with open(entry) as input_file:
            data = input_file.read()
        if entry.endswith('.png'): # images must be encoded
            data = base64.b64encode(data)
        element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
        element_list.append(element)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)

    
normal_hrs = {}
maintain_hrs = {}
def sethours():
    print("Enter Hours:")
    print("Proper form: 10 <Enter> 15 (10AM to 3PM)")
    print("You can Exit by entering 0")
    while True:
        from_h = int(input("From:"))
        if from_h <= 0:
            break
        to_h = int(input("To:"))
        if to_h <= 0:
            break
        normal_hrs[from_h] = to_h
    for time in normal_hrs:
        print("You have access to water from {0} To {1}".format(time, normal_hrs[time]))
def writefile():
    html_page = Airium()
    # Generating HTML file
    html_page('<!DOCTYPE html>')
    with html_page.html(lang="en"):
        with html_page.head():
            html_page.meta(charset="utf-8")
            html_page.title(_t="Example: How to use Airium library")
        with html_page.body():
            with html_page.h1(id="id23345225", kclass='main_header'):
                html_page("Hello Finxters")
    # Casting the file to a string to extract the value
    html = str(html_page)
    with open('index.html', 'wb') as file_handle:
        file_handle.write(bytes(html, encoding='utf8'))

def menu():
    while True:
        print("List of Available Commands:")
        print("1.Set Hours for Today")
        print("2.Set Maintenance Date and Hours")
        print("3.Get Status and Write to file")
        print("4.Push changes to server")
        print("5.Exit")
        R = input()
        if R == "1":
            sethours()
        elif R == "2":
            pass
        elif R == "3":
            pass
        elif R == "4":
            pushhub()
        elif R == "5":
            return 0
login()
menu()