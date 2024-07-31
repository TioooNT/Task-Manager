from Classes import User, Task, Category
from Manipulators import Func, Output, Interaction


Operator = Func()
Interact = Interaction()

def main():
    user: User = None
    while True:
        while user is None: # Not logged in
            Output.login_Menu()
            choice = input('Enter your choice: ')

            if choice == '1':
                user = Interact.login()

            elif choice == '2':
                full_name = input('Enter your full name: ')
                username = input('Enter your username: ')
                password = input('Enter your password: ')
                if password != input('Re-enter your password: '):
                    print('Passwords do not match')
                    continue
                else:
                    Operator.create_User(full_name, username, password)

            elif choice == '3':
                return

            else:
                print('Invalid choice')


        while user is not None: # Logged in
            Output.main_Menu()
            choice = input('Enter your choice: ')
            if choice == '1':
                title = input('Enter the title of the task: ')
                content = input('Enter the content of the task: ')
                Output.category_Menu(user.id)
                category_id = Interact.choose_Category(user.id)

                while category_id is None:
                    print('No categories found, please choose a category again')
                    category_id = Interact.choose_Category(user.id)
                Operator.create_Task(title=title, content=content, author_id=user.id, category_id=category_id)
            
            elif choice == '2':
                name = input('Enter the name of the category: ')
                Output.category_Menu(user.id)
                Operator.create_Category(name=name, author_id=user.id)
            
            elif choice == '3':
                Interact.display_Tasks(author_id=None)

            elif choice == '4':
                Interact.display_Tasks(author_id=user.id)
            
            elif choice == '5':
                Interact.search_Task(author_id=user.id)
            
            elif choice == '6':
                task_id = Interact.choose_Task(author_id=user.id)
                if task_id is None:
                    print('No tasks found')
                    continue
                Output.modification_Menu()
                choice = input('Enter your choice: ')

                if choice == '1':
                    content = input('Enter the new content: ')
                    Operator.change_Task_Content(task_id=task_id, new_content=content)

                elif choice == '2':
                    Operator.change_Task_Status(task_id=task_id)

                elif choice == '3':  
                    Operator.delete_Task(task_id=task_id)
                
                else:
                    print('Invalid choice')
            
            elif choice == '7':
                user = None


if __name__ == '__main__':
    main()