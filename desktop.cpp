#include <windows.h>
#include <commctrl.h>
#include <ShlObj.h>
#include <stdio.h>
#include <vector>
#include <exception>

class Desktop {
public:
    Desktop();

    bool deleteItem(int);
    int intersect(int left, int top, int width, int height);
    void printItemPositions() const;

private:
    HWND m_progman;
    HWND m_shell;
    HWND m_listView;

    std::vector<POINT> m_itemPositions;
};

Desktop::Desktop() {
    m_progman = FindWindow("progman", NULL);
    m_shell = FindWindowEx(m_progman, NULL, "shelldll_defview", NULL);
    m_listView = FindWindowEx(m_shell, NULL, "syslistview32", NULL);
    int itemCount = ListView_GetItemCount(m_listView);

    m_itemPositions.assign(itemCount, POINT{});

    DWORD desktopProcId = 0;
    GetWindowThreadProcessId(m_listView, &desktopProcId);
    HANDLE desktopProcHandle = OpenProcess(PROCESS_VM_OPERATION | PROCESS_VM_READ, FALSE, desktopProcId);
    if (!desktopProcHandle) {
        throw std::exception("OpenProcess error");
    }

    LPVOID ptMem = (LPPOINT)VirtualAllocEx(desktopProcHandle, NULL, sizeof(POINT), MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (!ptMem) {
        CloseHandle(desktopProcHandle);
        throw std::exception("VirtualAllocEx error");
    }

    for (int i = 0;i < itemCount;i++) {
        if (!ListView_GetItemPosition(m_listView, i, ptMem)) {
            throw std::exception("GetItemPosition error");
            continue;
        }

        if (!ReadProcessMemory(desktopProcHandle, ptMem, &m_itemPositions[i], sizeof(POINT), nullptr)) {
            throw std::exception("ReadProcessMemory error");
            continue;
        }
    }

    VirtualFreeEx(desktopProcHandle, ptMem, 0, MEM_RELEASE);
    CloseHandle(desktopProcHandle);
}

bool Desktop::deleteItem(int index) {
    if (!ListView_DeleteItem(m_listView, index)) {
        return false;
    }
    return true;
}

void Desktop::printItemPositions() const {
    for (const auto& point : m_itemPositions) {
        printf("(%d, %d)\n", point.x, point.y);
    }
}

int Desktop::intersect(int left, int top, int width, int height) {
    int count = 0;
    for (int i = 0;i < m_itemPositions.size();i++) {
        int x = m_itemPositions[i].x,
            y = m_itemPositions[i].y;
        if (x >= left && x <= left + width &&
            y >= top && y <= top + height) {
            // Intersection
            bool res = deleteItem(i);
            count++;
        }
    }
    return count;
}

int main() {
    Desktop desk;
    desk.printItemPositions();

    return 0;
}
