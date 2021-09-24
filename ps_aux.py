from parsing import *
import time


if __name__ == '__main__':
    processes, stdout = parse_ps_aux()
    users: List[str] = get_users(processes)
    users_processes_report = str()
    for user in users:
        users_processes = [process for process in processes if process.user == user]
        users_processes_report += f"\t{user}: {len(users_processes)}\n"
    full_mem_used = sum([process.mem for process in processes])
    full_cpu_used = sum([process.cpu for process in processes])
    mem_sorted_list = sorted(processes, key=lambda process: process.mem, reverse=True)
    cpu_sorted_list = sorted(processes, key=lambda process: process.cpu, reverse=True)
    report = f"Отчет о состоянии системы\n" \
             f"\n" \
             f"Пользователи системы: {str('; ').join(users)}\n" \
             f"Процессов запущено: {len(processes)}\n" \
             f"\n" \
             f"Пользовательских процессов\n" \
             f"{users_processes_report}" \
             f"\n" \
             f"Всего памяти используется: {full_mem_used:.2f} Mb\n" \
             f"Всего CPU используется: {full_cpu_used:.2f} %\n" \
             f"Больше всего памяти использует: {mem_sorted_list[0].command[:20]}\n" \
             f"Больше всего CPU использует: {cpu_sorted_list[0].command[:20]}"
    print(report)
    current_time = time.localtime(time.time())
    current_time_str = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    report_file_name = f"{current_time_str}_report.txt"
    stdout_file_name = f"{current_time_str}_ps_aux.txt"
    with open(report_file_name, 'w') as file:
        file.write(report)
    print(f"\nОтчет был записан в файл {report_file_name}")
    with open(stdout_file_name, 'w') as file:
        file.write(stdout)
    print(f"Вывод команды ps aux был записал в файл {stdout_file_name}")

