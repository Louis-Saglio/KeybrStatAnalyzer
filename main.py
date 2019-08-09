from statistics import mean

from matplotlib import pyplot as plt

from constants import DATA_FILE_PATH


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


def compute_batch_size(sample_proportion: int, collection_length):
    batch_size_1 = collection_length / sample_proportion
    batch_size_1 = int(batch_size_1)
    if batch_size_1 % 2 == 0:
        batch_size_1 += 1
    return batch_size_1


def parse(file_path):
    time_to_type_by_char_code = {"all": []}
    miss_count_by_char_code = {"all": []}
    with open(file_path) as file:
        char_code = None
        session_times_to_type = []
        session_misses_count = []
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
                miss_count_by_char_code["all"].append(mean(session_misses_count))
                session_misses_count.clear()
            elif "missCount" in line:
                if char_code not in miss_count_by_char_code:
                    miss_count_by_char_code[char_code] = []
                miss_count = int(line[:-2].split(":")[1])
                miss_count_by_char_code[char_code].append(miss_count)
                session_misses_count.append(miss_count)
    return time_to_type_by_char_code, miss_count_by_char_code


def plot(time_to_type_by_char_code, miss_count_by_char_code):
    for char_code, times_to_type in time_to_type_by_char_code.items():
        plt.title(chr(char_code) if char_code != "all" else "all")
        len_times_to_type = len(times_to_type)
        plt.plot(soft_number_list(times_to_type, compute_batch_size(50, len_times_to_type)))
        plt.plot(soft_number_list(times_to_type, compute_batch_size(3, len_times_to_type)))
        plt.show()
    for char_code, misses_count in miss_count_by_char_code.items():
        plt.title((chr(char_code) if char_code != "all" else "all") + " miss count")
        plt.plot(soft_number_list(misses_count, compute_batch_size(50, len(misses_count))))
        plt.plot(soft_number_list(misses_count, compute_batch_size(3, len(misses_count))))
        plt.show()


if __name__ == '__main__':
    plot(*parse(DATA_FILE_PATH))
