#include <windows.h>
#include <commctrl.h>
#include <ShlObj.h>
#include <stdio.h>
#include <vector>
#include <exception>

class Desktop {
public:
    Desktop();
    ~Desktop();

    int intersect(int left, int top, int width, int height);
    void printItemPositions();

private:
    bool deleteItem(int);
    std::vector<POINT> getItemPositions();

    HWND m_progman;
    HWND m_shell;
    HWND m_listView;

    HANDLE h_desktopProc;
    LPVOID p_pointMem;
};

Desktop::Desktop() {
    m_progman = FindWindow("progman", NULL);
    m_shell = FindWindowEx(m_progman, NULL, "shelldll_defview", NULL);
    m_listView = FindWindowEx(m_shell, NULL, "syslistview32", NULL);

    DWORD desktopProcId = 0;
    GetWindowThreadProcessId(m_listView, &desktopProcId);
    h_desktopProc = OpenProcess(PROCESS_VM_OPERATION | PROCESS_VM_READ, FALSE, desktopProcId);
    if (!h_desktopProc) {
        throw std::exception("OpenProcess error");
    }

    p_pointMem = VirtualAllocEx(h_desktopProc, NULL, sizeof(POINT), MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (!p_pointMem) {
        CloseHandle(h_desktopProc);
        throw std::exception("VirtualAllocEx error");
    }
}

std::vector<POINT> Desktop::getItemPositions() {
    int itemCount = ListView_GetItemCount(m_listView);
    std::vector<POINT> itemPositions(itemCount, POINT{});

    for (int i = 0;i < itemCount;i++) {
        if (!ListView_GetItemPosition(m_listView, i, p_pointMem)) {
            throw std::exception("GetItemPosition error");
            continue;
        }
        if (!ReadProcessMemory(h_desktopProc, p_pointMem, &itemPositions[i], sizeof(POINT), NULL)) {
            throw std::exception("ReadProcessMemory error");
            continue;
        }
    }
    return itemPositions;
}

Desktop::~Desktop() {
    VirtualFreeEx(h_desktopProc, p_pointMem, 0, MEM_RELEASE);
    CloseHandle(h_desktopProc);
}

bool Desktop::deleteItem(int index) {
    if (!ListView_DeleteItem(m_listView, index)) {
        return false;
    }
    return true;
}

void Desktop::printItemPositions() {
    auto itemPositions = getItemPositions();
    for (const auto& point : itemPositions) {
        printf("(%d, %d)\n", point.x, point.y);
    }
}

int Desktop::intersect(int left, int top, int width, int height) {
    int count = 0;
    while (true) {
        int index = -1;
        auto itemPositions = getItemPositions();
        for (int i = 0;i < itemPositions.size();i++) {
            int x = itemPositions[i].x,
                y = itemPositions[i].y;
            if (x >= left && x <= left + width &&
                y >= top && y <= top + height) {
                index = i;
                break;
            }
        }

        if (index != -1) {
            printf("Deleting %d: (%d,%d)\n", index, itemPositions[index].x, itemPositions[index].y);
            // Intersection
            bool res = deleteItem(index);
            count++;
        } else {
            break;
        }
    }
    return count;
}

int main() {
    Desktop desk;
    desk.printItemPositions();

    return 0;
}
