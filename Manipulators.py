from typing import Optional
from Models import session, engine
from Classes import User, Task, Category

class Checker:

    @staticmethod
    def user_Exist(username: str) -> bool:
        return session.query(User).filter(User.username == username).first() is not None


    @staticmethod
    def task_Exist(title: str, author_id: int) -> bool:
        return session.query(Task).filter(Task.title == title).filter(Task.author_id==author_id).first() is not None
    

    @staticmethod
    def category_Exist(name: str, author_id: int) -> bool:
        return session.query(Category).filter(Category.name == name).filter(Category.author_id==author_id).first() is not None


class Output:
    
    @staticmethod
    def login_Menu():
        print('-'*30)
        print('1. Login')
        print('2. Register')
        print('3. Exit')


    @staticmethod
    def main_Menu():
        print('-'*30)
        print('1. Create Task')
        print('2. Create Category')
        print("3. Display all user's Tasks")
        print('4. Display my Tasks')
        print('5. Search Task')
        print('6. Modify Task')
        print('7. Log out')
    

    @staticmethod
    def modification_Menu():
        print('-'*30)
        print('1. Change content')
        print('2. Change status')
        print('3. Delete task')


    @staticmethod
    def category_Menu(author_id: int) -> None:
        print('-'*30)
        Categories = session.query(Category).filter(Category.author_id == author_id).all()
        if Categories is None:
            print('No categories available')
            return
        print('Categories:')
        for category in Categories:
            print(f'{category.id}. {category.name}')



class Func: # Functions that interact directly with the database

    def create_User(self, full_name: str, username: str, password: str) -> None:
        user = User(full_name=full_name, username=username, password=password)
        if Checker.user_Exist(username=username):
            print('User already exists, please choose another username')
        else:
            session.add(user)
            session.commit()
            session.add(Category(name='None', author_id=user.id)) # Create a default category for the user's task
            session.commit()
        

    def create_Task(self, title: str, content: str, author_id: int, category_id: int) -> None:
        task = Task(title=title, content=content, author_id=author_id, category_id=category_id)
        if Checker.task_Exist(title=title, author_id=author_id):
            print("Task's title already exists")
        else:
            session.add(task)
            session.commit()
    

    def create_Category(self, name: str, author_id: int) -> None:
        category = Category(name=name, author_id=author_id)
        if Checker.category_Exist(name=name, author_id=author_id):
            print('Category already exists')
        else:
            session.add(category)
            session.commit()
    

    def find_User(self, full_name: Optional[str], username: Optional[str]) -> User:
        user_query = session.query(User)

        if full_name is None:
            user = user_query.filter(User.username == username).first()
        elif username is None:
            user = user_query.filter(User.full_name == full_name).first()

        if user is None:
            print('User not found')
            return None
        
        return user


    def change_Task_Content(self, task_id: int, new_content: str) -> None:
        task: Task | None = session.query(Task).get(task_id)
        if task is None:
            print('Task not found')
        else:
            task.content = new_content
            print("Task's content changed successfully")
            session.commit()
    

    def change_Task_Status(self, task_id: int) -> None:
        task: Task | None = session.query(Task).get(task_id)
        if task is None:
            print('Task not found')
        else:
            task.status = not task.status
            print(f"Task's status changed to {task.status}")
            session.commit()
    

    def delete_Task(self, task_id: int) -> None:
        task: Task | None = session.query(Task).get(task_id)
        if task is None:
            print('Task not found')
        else:
            session.delete(task)
            session.commit()

        


        
class Interaction: # Functions that interact with the user
    
    def login(self) -> User:
        print('-'*30)
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        user: User | None = session.query(User).filter(User.username == username).filter(User.password == password).first()

        if user is None:
            print('Invalid username or password')
        else:
            print('Logged in successfully')
        return user


    def display_Tasks(self, author_id: Optional[int]) -> None:
        tasks_query = session.query(Task)

        if author_id is not None: # Display tasks of a specific 
            tasks_query = tasks_query.filter(Task.author_id == author_id)

        tasks = tasks_query.order_by(Task.dateAdded.desc()).all() # Get all tasks descendingly

        while True:
            print('-'*30)
            page = input(f'Enter the page number (/{int(len(tasks)/10)} pages): ')
            try:
                page = int(page)
                start = (page-1)*10
                end = page*10

                if len(tasks)-1 >= start and start >= 0:
                    print(f'Page {page}/{int(len(tasks)/10)}:')
                    for index in range(start, min(end, len(tasks))):
                        task = tasks[index]
                        print(f'{task.id}. Author: {task.author.username}\nTitle: {task.title}\nContent: {task.content}\nStatus: {task.status}\n')
                else:
                    print('No tasks found')

                show_more = None
                while show_more not in ['y', 'n']:
                    show_more = input('Do you want to see other pages? (y/n): ')
                
                if show_more == 'n':
                    break

            except ValueError:
                print("Invalid input. Please enter a valid number.")
    

    def search_Task(self, author_id: int) -> None:
        while True:
            print('-'*30)
            print('Search by:')
            print('1. Title')
            print('2. Content')
            choice = input('Enter your choice: ')

            if choice == '1':
                title = input('Enter the title: ')
                tasks = session.query(Task).filter(Task.title.like(f'%{title}%')).all()

            elif choice == '2':
                content = input('Enter the content: ')
                tasks = session.query(Task).filter(Task.content.like(f'%{content}%')).all()

            if tasks is None:
                print('Task not found')

            else:
                for task in tasks:
                    print(f'{task.id}. Author: {task.author.username}\nTitle: {task.title}\nContent: {task.content}\nStatus: {task.status}\n')
            
            show_more = None
            while show_more not in ['y', 'n']:
                show_more = input('Do you want to search for other tasks? (y/n): ')
            
            if show_more == 'n':
                break


    def choose_Task(self, author_id: int) -> int:
        print('-'*30)
        task_id = input('Enter the task id: ')
        try:
            task_id = int(task_id)
            task: Task | None = session.query(Task).filter(Task.id == task_id, Task.author_id == author_id).first()
            return None if task == None else task.id
        
        except:
            print('Invalid task id')
            return None


    def choose_Category(self, author_id: int) -> int:
        print('-'*30)
        category_id = input('Enter the category id: ')
        try:
            category_id = int(category_id)
            category: Category | None = session.query(Category).filter(Category.id == category_id, Category.author_id == author_id).first()
            return None if category == None else category.id
        
        except ValueError:
            print('Invalid category id')
            return None


