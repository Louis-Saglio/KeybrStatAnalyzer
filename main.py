from statistics import mean

from matplotlib import pyplot as plt

from constants import DATA_FILE_PATH

time_to_type_by_char_code = {"all": []}


def soft_number_list(numbers: list, batch_size: int):
    assert batch_size % 2 == 1, "batch_size must not be even"
    numbers_size = len(numbers)
    assert numbers_size >= batch_size
    soft_list = []
    half_batch_size = batch_size // 2
    for i in range(half_batch_size, numbers_size - half_batch_size):
        numbers_to_merge = [numbers[n] for n in range(i - half_batch_size, i + half_batch_size + 1)]
        avg = mean(numbers_to_merge)
        soft_list.append(avg)
    return soft_list


with open(DATA_FILE_PATH) as file:
    char_code = None
    session_times_to_type = []
    for line in file:
        if "charCode" in line:
            char_code = int(line[:-2].split(":")[1])
        elif "timeToType" in line:
            if char_code not in time_to_type_by_char_code:
                time_to_type_by_char_code[char_code] = []
            time_to_type = int(line[:-1].split(":")[1])
            time_to_type_by_char_code[char_code].append(time_to_type)
            session_times_to_type.append(time_to_type)
        elif "histogram" in line and session_times_to_type:
            time_to_type_by_char_code["all"].append(mean(session_times_to_type))
            session_times_to_type.clear()


print("size", "batch_size", "ratio len / batch")
for char_code, times_to_type in time_to_type_by_char_code.items():
    plt.title(chr(char_code) if char_code != "all" else "all")
    len_times_to_type = len(times_to_type)
    batch_size = len(times_to_type) / 5
    batch_size = int(batch_size)
    if batch_size % 2 == 0:
        batch_size += 1
    print(len(times_to_type), batch_size, len(times_to_type) / batch_size)
    plt.plot(soft_number_list(times_to_type, batch_size))
    plt.show()
