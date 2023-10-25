import os
import multiprocessing
import random
import time


x = random.randint(0,3)

folder_path = r"C:\Store_Migration"  # Replace with the actual path to your folder

def run_script(file_path):
    print(f"Running {file_path}...")
    os.system(f'python "{file_path}"')

if __name__ == '__main__':
    processes = []
    
    for i in range(1, 5):
        file_name = f'kwt_{i}.py'
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            process = multiprocessing.Process(target=run_script, args=(file_path,))
            processes.append(process)
            process.start()
            # time.sleep(0.5)
        else:
            print(f"{file_name} does not exist.")

    for process in processes:
        process.join()