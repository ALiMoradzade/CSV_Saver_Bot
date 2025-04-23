import csv

column_names = [
    "نام تامین کننده",
    "نام محصول",
    "قیمت روز",
    "شرایط پرداخت"
]
path = "database.csv"


def clear():
    open(path, 'w').close()


def init_header():
    with open(path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=column_names)
        writer.writeheader()


def append(new_record: list, unique_records: bool = True):
    init_header()

    # read
    records = read()
    is_duplicate: bool = False

    if unique_records:
        if new_record in records:
            is_duplicate = True

    # Write
    if unique_records and is_duplicate:
        return "it is existed!"
    else:
        with open(path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_record)
        return "successful"


def read() -> list:
    with open(path, mode='r', newline='', encoding='utf-8') as file:
        content = csv.reader(file)
        records = list(content)
        return records

