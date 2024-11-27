import csv
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from typing import List, Tuple, Set, Dict

class MangMayTinh:
    def __init__(self):
        self.mang: Dict[int, Set[int]] = defaultdict(set)
        self.da_tham: Set[int] = set()

    def them_ket_noi(self, may1: int, may2: int):
        """
        Thêm kết nối hai chiều giữa hai máy tính.
        """
        self.mang[may1].add(may2)
        self.mang[may2].add(may1)

    def dfs(self, may_hien_tai: int):
        """
        Thực hiện DFS từ máy hiện tại.
        """
        self.da_tham.add(may_hien_tai)
        for may_ke in self.mang[may_hien_tai]:
            if may_ke not in self.da_tham:
                self.dfs(may_ke)

    def kham_pha_mang(self, may_bat_dau: int):
        """
        Khám phá mạng từ máy bắt đầu sử dụng DFS.
        """
        self.da_tham.clear()
        self.dfs(may_bat_dau)

    def tim_may_khong_truy_cap_duoc(self) -> Set[int]:
        """
        Tìm các máy tính không thể truy cập từ máy chủ ban đầu.
        """
        tat_ca_may = set(self.mang.keys())
        return tat_ca_may - self.da_tham

    def tinh_tong_ket_noi(self) -> int:
        """
        Tính tổng số kết nối trong mạng.
        """
        return sum(len(ket_noi) for ket_noi in self.mang.values()) // 2

def doc_du_lieu_csv(ten_file: str) -> Tuple[List[Tuple[int, int]], Set[int]]:
    """
    Đọc dữ liệu kết nối từ file CSV và trả về danh sách kết nối và tập hợp các máy chủ.
    """
    ket_noi = []
    tat_ca_may = set()
    try:
        with open(ten_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Bỏ qua hàng tiêu đề
            for row_number, row in enumerate(csv_reader, start=2):
                if len(row) != 2:
                    print(f"Lỗi ở dòng {row_number}: Số cột không đúng. Cần 2 cột, nhưng có {len(row)} cột.")
                    continue
                try:
                    may1, may2 = map(int, row)
                    ket_noi.append((may1, may2))
                    tat_ca_may.add(may1)
                    tat_ca_may.add(may2)
                except ValueError:
                    print(f"Lỗi ở dòng {row_number}: Không thể chuyển đổi dữ liệu sang số nguyên.")
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file '{ten_file}'")
    except Exception as e:
        print(f"Lỗi không xác định khi đọc file: {e}")
    
    if not ket_noi:
        print("Cảnh báo: Không có dữ liệu kết nối hợp lệ được đọc từ file.")

    return ket_noi, tat_ca_may

def mo_ta_thuat_toan_duyet_do_thi():
    """Mô tả các thuật toán duyệt đồ thị."""
    print("Mô tả các thuật toán duyệt đồ thị:")
    print("1. Duyệt theo chiều sâu (DFS - Depth-First Search):")
    print("   - Bắt đầu từ một đỉnh, đi sâu nhất có thể trước khi quay lui.")
    print("   - Sử dụng ngăn xếp hoặc đệ quy để thực hiện.")
    print("   - Thích hợp cho việc tìm đường đi, kiểm tra liên thông, và nhiều bài toán khác.")
    print("\n2. Duyệt theo chiều rộng (BFS - Breadth-First Search):")
    print("   - Bắt đầu từ một đỉnh, thăm tất cả các đỉnh lân cận trước khi đi sâu hơn.")
    print("   - Sử dụng hàng đợi để thực hiện.")
    print("   - Thích hợp cho việc tìm đường đi ngắn nhất trong đồ thị không có trọng số.")
    print("\nTrong bài toán này, chúng ta sử dụng DFS vì nó phù hợp cho việc khám phá mạng và kiểm tra tính liên thông.")

def hien_thi_cay_dfs(mang: MangMayTinh, may_bat_dau: int):
    """
    Hiển thị đồ thị gốc và cây DFS của mạng máy tính.

    :param mang: Đối tượng MangMayTinh
    :param may_bat_dau: Số máy chủ bắt đầu
    """
    def dfs_edges(graph, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        for next in set(graph[start]) - visited:
            yield (start, next)
            yield from dfs_edges(graph, next, visited)

    G = nx.Graph()

    # Thêm các cạnh vào đồ thị gốc
    for may, ket_noi in mang.mang.items():
        for may_ke in ket_noi:
            G.add_edge(may, may_ke)

    # Tạo cây DFS
    T = nx.Graph(list(dfs_edges(G, may_bat_dau)))

    # Tạo danh sách màu cho các nút
    mau_sac_G = ['red' if nut == may_bat_dau else 'lightblue' for nut in G.nodes()]
    mau_sac_T = ['red' if nut == may_bat_dau else 'green' for nut in T.nodes()]

    # Tạo figure với hai subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    # Vẽ đồ thị gốc
    vi_tri_G = nx.spring_layout(G)
    nx.draw(G, vi_tri_G, node_color=mau_sac_G, with_labels=True, node_size=500, 
            font_size=10, font_weight='bold', ax=ax1)
    ax1.set_title("Đồ thị gốc")

    # Vẽ cây DFS
    vi_tri_T = nx.spring_layout(T)
    nx.draw(T, vi_tri_T, node_color=mau_sac_T, with_labels=True, node_size=500, 
            font_size=10, font_weight='bold', ax=ax2)
    ax2.set_title("Cây DFS")

    # Thêm chú thích
    diem_do = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=15)
    diem_xanh_nhat = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightblue', markersize=15)
    diem_xanh_la = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=15)
    fig.legend([diem_do, diem_xanh_nhat, diem_xanh_la], 
               ["Máy chủ bắt đầu", "Các máy trong đồ thị gốc", "Máy có thể truy cập (DFS)"],
               loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=3)

    # Điều chỉnh bố cục
    plt.tight_layout()
    plt.show()

def luu_ket_qua(mang: MangMayTinh, may_bat_dau: int, may_khong_truy_cap_duoc: Set[int], tong_ket_noi: int):
    with open('ket_qua.txt', 'w', encoding='utf-8') as file:
        file.write(f"Máy chủ bắt đầu: {may_bat_dau}\n")
        file.write(f"Các máy có thể truy cập: {sorted(mang.da_tham)}\n")
        file.write(f"Các máy không thể truy cập: {sorted(may_khong_truy_cap_duoc)}\n")
        file.write(f"Tổng số kết nối trong mạng: {tong_ket_noi}\n")

# Chương trình chính
if __name__ == "__main__":
    mang = MangMayTinh()

    # Đọc kết nối từ file CSV
    ket_noi, tat_ca_may = doc_du_lieu_csv('chude2.csv')

    if not ket_noi:
        print("Không có dữ liệu kết nối hợp lệ. Chương trình kết thúc.")
        exit()

    print(f"Đã đọc được {len(ket_noi)} kết nối hợp lệ.")

    # Thêm các kết nối vào mạng
    for may1, may2 in ket_noi:
        mang.them_ket_noi(may1, may2)

    mo_ta_thuat_toan_duyet_do_thi()

    print("\nKhám phá mạng:")
    while True:
        try:
            may_bat_dau = int(input("Nhập số máy chủ bắt đầu: "))
            if may_bat_dau not in mang.mang:
                print("Lỗi: Máy chủ không tồn tại trong mạng. Vui lòng thử lại.")
                continue
            break
        except ValueError:
            print("Lỗi: Vui lòng nhập một số nguyên hợp lệ.")

    # Thực hiện khám phá mạng từ máy chủ bắt đầu
    mang.kham_pha_mang(may_bat_dau)

    print(f"\nCác máy tính có thể truy cập từ máy chủ {may_bat_dau}: {sorted(mang.da_tham)}")

    # Tính tổng số kết nối trong mạng
    tong_ket_noi = mang.tinh_tong_ket_noi()
    print(f"\nTổng số kết nối trong mạng: {tong_ket_noi}")

    # Hiển thị các máy chủ không tồn tại trong dữ liệu file
    may_khong_ton_tai = set(range(1, max(tat_ca_may) + 1)) - tat_ca_may
    print(f"\nCác máy chủ không tồn tại trong dữ liệu file chude2.csv: {sorted(may_khong_ton_tai)}")

    # Tìm các máy không truy cập được
    may_khong_truy_cap_duoc = mang.tim_may_khong_truy_cap_duoc()

    # Lưu kết quả vào file
    luu_ket_qua(mang, may_bat_dau, may_khong_truy_cap_duoc, tong_ket_noi)
    print("\nKết quả đã được lưu vào file 'ket_qua.txt'")

    # Hiển thị cây DFS
    hien_thi_cay_dfs(mang, may_bat_dau)
