import random
import sys
sys.path.append('models')
from faker import Faker
from models.todo import Todo
from config.config import DATABASE

todo = Todo(DATABASE)

def create_fake_tasks(n):
    """Generate fake users."""
    generic_tasks = ['call to ', 'email to ', 'text to ', 'call from ', 'email from ', 'text from ']
    faker = Faker()
    for i in range(n):
        data = {
            'task': random.choice(generic_tasks) + faker.name(), 
            'status': random.choice([0, 1])
        }
        todo.insert(data)
        
    print(f'Added {n} fake tasks to the database.')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Pass the number of users you want to create as an argument.')
        sys.exit(1)
    create_fake_tasks(int(sys.argv[1]))