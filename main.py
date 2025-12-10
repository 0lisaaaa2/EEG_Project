from config import subjects, tasks
import s_00_fetch_data

if __name__ == "__main__":
    for subject in subjects:
        for task in tasks:
            raw = s_00_fetch_data.load_data(subject, task)
            print(raw)
