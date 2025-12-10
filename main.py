from config import subjects
import s_00_fetch_data

if __name__ == "__main__":
    for subject in subjects:
        raw = s_00_fetch_data.load_data("ds005841-download")
        print(raw)


