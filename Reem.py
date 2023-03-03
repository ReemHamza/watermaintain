from datetime import datetime # date library
from github import Github # library for interacting with Github API
from github import InputGitTreeElement # library for interacting with Github API
from airium import Airium # library for generating and generating html pages

week_days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
week_prog = {week_days[0]:[0,{}],week_days[1]:[1,{}],week_days[2]:[0,{}],week_days[3]:[0,{}],week_days[4]:[0,{}],week_days[5]:[0,{}],week_days[6]:[0,{}]}
token = ""
def store_token():
    global token
    token = input("Enter Your API Token:\n")
def pushhub(login):
    git = Github(login)
    repo = git.get_user().get_repo('watermaintain')
    file_list = ['index.html']#C://Users//Administrator//Desktop//Project//
    file_names = ['index.html']
    commit_message = "Schedule for {}".format(datetime.now())
    master_ref = repo.get_git_ref('heads/main')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    element_list = list()
    for i, entry in enumerate(file_list):
        with open(entry) as input_file:
            data = input_file.read()
        element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
        element_list.append(element)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)
def writefile():
    html_page = Airium()
    html_page('<!DOCTYPE html>')
    with html_page.html(lang="en"):
        with html_page.head():
            html_page.meta(charset="utf-8")
            html_page.link(href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css",rel="stylesheet",integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD",crossorigin="anonymous")
            html_page.script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js",integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN",crossorigin="anonymous")
            html_page.title(_t="Water Information Outlet")
        with html_page.body():
            with html_page.h1(klass="d-flex p-2 justify-content-center"):
                html_page("Water Information Outlet: {}".format(datetime.now().date()))
            with html_page.div(klass="d-flex p-5"):
                for day in week_days:
                    print(week_prog.get(day))
                    if week_prog.get(day)[0] == 1:
                        with html_page.div(klass = "d-flex p-2 justify-content-center alert alert-warning"):
                            html_page("{} <br>Outage due to maintenance".format(day))
                    if week_prog.get(day)[0] == 0:
                        with html_page.div(klass = "d-flex p-2 justify-content-center alert alert-primary"):
                            html_page("{} <br>".format(day))
                            for keypair in week_prog.get(day)[1]:
                                html_page("Available from {} to {} <br>".format(keypair,week_prog.get(day)[1].get(keypair)))
                                                    
    html = str(html_page)
    with open('index.html', 'wb') as file_handle:
        file_handle.write(bytes(html, encoding='utf8'))
def setday(day):
    m_input = input("Is there maintenance? y for yes, n for no\n")
    if m_input == "y":
        week_prog[week_days[day-1]][0] = 1
    else:
        week_prog[week_days[day-1]][0] = 0
        print("Enter Hours:")
        print("Proper format: 10 <Enter> 15 (10AM to 3PM)")
        print("You can Exit by entering 0")
        while True:
            from_h = int(input("From:"))
            if from_h <= 0:
                break
            elif from_h > 24 or from_h < 0:
                print("INVALID INPUT - Can't Enter more than 24 or less than 0")
                break
            to_h = int(input("To:"))
            if to_h <= 0:
                break
            elif to_h > 24 or to_h < 0:
                print("INVALID INPUT - Can't Enter more than 24 or less than 0")
                break
            elif to_h >= from_h:
                print("INVALID INPUT - To should be more than From")
            week_prog[week_days[day-1]][1][from_h] = to_h
def selectday():
    print("1.Sunday")
    print("2.Monday")
    print("3.Tuesday")
    print("4.Wednesday")
    print("5.Thursday")
    print("6.Friday")
    print("7.Sturday")
    u_input = input()
    if u_input == "1":
        setday(int(u_input))
    elif u_input == "2":
        setday(int(u_input))
    elif u_input == "3":
        setday(int(u_input))
    elif u_input == "4":
        setday(int(u_input))
    elif u_input == "5":
        setday(int(u_input))
    elif u_input == "6":
        setday(int(u_input))
    elif u_input == "7":
        setday(int(u_input))
def menu():
    while True:
        for i in week_prog:
            print(i)
            print(week_prog.get(i)[1])
        print("List of Available Commands:")
        print("1.Set Maintenance Date and Hours")
        print("2.Generate HTML file")
        print("3.Push HTML file to server")
        print("4.Exit")
        R = input()
        if R == "1":
            selectday()
            while(True):
                u_input = input("Do you want to enter another date? y for yes, n for no\n")
                if u_input == "y":
                    selectday()
                else:
                    break
        elif R == "2":
            writefile()
        elif R == "3":
            pushhub(token)
        elif R == "4":
            return 0
store_token()
menu()