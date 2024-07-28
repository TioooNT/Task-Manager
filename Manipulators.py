from Models import session, engine
from Classes import User, Task, Category

class Checker:

    @staticmethod
    def user_Exist(username: str) -> bool:
        return session.query(User).filter(User.username == username).first() is not None


    @staticmethod
    def task_Exist(title: str) -> bool:
        return session.query(Task).filter(Task.title == title).first() is not None
    

    @staticmethod
    def category_Exist(name: str) -> bool:
        return session.query(Category).filter(Category.name == name).first() is not None


class Output:
    pass


class Func:

    def create_User(self, full_name: str, username: str, password: str) -> None:
        user = User(full_name=full_name, username=username, password=password)
        if Checker.user_Exist(username):
            print('User already exists')
        else:
            session.add(user)
            session.commit()
        

    def create_Task(self, title: str, content: str, author_id: int, category_id: int) -> None:
        task = Task(title=title, content=content, author_id=author_id, category_id=category_id)
        if Checker.task_Exist(title):
            print("Task's title already exists")
        else:
            session.add(task)
            session.commit()
    

    def create_Category(self, name: str) -> None:
        category = Category(name=name)
        if Checker.category_Exist(name):
            print('Category already exists')
        else:
            session.add(category)
            session.commit()


    def change_Task_Content(self, title: str, author_id: int, new_content: str) -> None:
        task = session.query(Task).filter(Task.title == title).filter(Task.author_id == author_id).first()
        if task is None:
            print('Task not found')
        else:
            task.content = new_content
            session.commit()
    

    def change_Task_Status(self, author_id: int ,title: str) -> None:
        task = session.query(Task).filter(Task.title == title).filter(Task.author_id == author_id).first()
        if task is None:
            print('Task not found')
        else:
            task.status = not task.status
            session.commit()
    

    def display_User_Tasks(self, author_id: int) -> None:
        tasks = session.query(Task).all()
        limit = 10 # Number of tasks to display per page

        while True:
            page = input(f'Enter the page number (/{int(len(tasks)/10)} pages): ')
            try:
                page = int(page)
                start = (page-1)*10
                end = page*10

                if len(tasks)-1 < start:
                    print('No tasks found')
                    continue
                
                print(f'Page {page}/{int(len(tasks)/10)}:')
                for index in range(start, end):
                    task = tasks[index]
                    print(f'{task.id}. Author: {task.author.username}\nTitle: {task.title}\nContent: {task.content}\nStatus: {task.status}\n')
                
                if input('Do you want to other pages? (y/n): ') == 'n':
                    break

            except:
                print("Invalid input. Please enter a valid number.")
        
    
    


    
    
