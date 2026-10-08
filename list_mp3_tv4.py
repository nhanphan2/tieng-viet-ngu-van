"""
Liet ke file mp3 trong thu muc tieng-viet-4 theo thu tu bai,
dong thoi tao san shortcode [audio_task] de dan vao web.

Chay:
    python list_mp3_tv4.py                       quet thu muc mac dinh (FOLDER ben duoi)
    python list_mp3_tv4.py D:\\duong\\dan\\khac   quet thu muc khac

Ket qua (ghi canh script):
    ds_mp3_tieng_viet_4.txt          danh sach ten file
    shortcode_tieng_viet_4.txt       cac dong [audio_task ...]
"""

import os
import re
import sys

FOLDER    = r"D:\7ball\file-doc-nv-tieng-viet\tieng-viet-4"
SUBDIR    = "tieng-viet-4"     # ten thu muc con trong repo GitHub
CDN       = "https://cdn.jsdelivr.net/gh/nhanphan2/tieng-viet-ngu-van"
OUT_DIR   = os.path.dirname(os.path.abspath(__file__))

# Ten bai co dau, dung lam label. Bai nao khong co ten se ghi "Bai N".
TEN_TAP1 = {
    1: "Điều kì diệu",
    2: "Thi nhạc",
    3: "Anh em sinh đôi",
    4: "Công chúa và người dẫn chuyện",
    5: "Thằn lằn xanh và tắc kè",
    6: "Nghệ sĩ trống",
    7: "Những bức chân dung",
    8: "Đò ngang",
    9: "Bầu trời trong quả trứng",
    10: "Tiếng nói của cỏ cây",
    11: "Tập làm văn",
    12: "Nhà phát minh 6 tuổi",
    13: "Con vẹt xanh",
    14: "Chân trời cuối phố",
    15: "Gặt chữ trên non",
    16: "Trước ngày xa quê",
    17: "Vẽ màu",
    18: "Đồng cỏ nở hoa",
    19: "Thanh âm của núi",
    20: "Bầu trời mùa thu",
    21: "Làm thỏ con bằng giấy",
    22: "Bức tường có nhiều phép lạ",
    23: "Bét-tô-ven và bản xô-nát Ánh trăng",
    24: "Người tìm đường lên các vì sao",
    25: "Bay cùng ước mơ",
    26: "Con trai người làm vườn",
    27: "Nếu em có một khu vườn",
    28: "Bốn mùa mơ ước",
    29: "Ở vương quốc tương lai",
    30: "Cánh chim nhỏ",
    31: "Nếu chúng mình có phép lạ",
    32: "Anh Ba",
}

TEN_TAP2 = {
    1: "Hải Thượng Lãn Ông",
    2: "Vệt phấn trên mặt bàn",
    3: "Ông Bụt đã đến",
    4: "Quả ngọt cuối mùa",
    5: "Tờ báo tường của tôi",
    6: "Tiếng ru",
    7: "Con muốn làm một cái cây",
    8: "Trên khóm tre đầu ngõ",
    9: "Sự tích con rồng cháu tiên",
    10: "Cảm xúc Trường Sa",
    11: "Sáng tháng Năm",
    12: "Chàng trai làng Phù Ủng",
    13: "Vườn của ông tôi",
    14: "Trong lời mẹ hát",
    15: "Người thầy đầu tiên của bố tôi",
    16: "Ngựa biên phòng",
    17: "Cây đa quê hương",
    18: "Bước mùa xuân",
    19: "Đi hội chùa Hương",
    20: "Chiều ngoại ô",
    21: "Những cánh buồm",
    22: "Cái cầu",
    23: "Đường đi Sa Pa",
    24: "Quê ngoại",
    25: "Khu bảo tồn động vật hoang dã Ngô-rông-gô-rô",
    26: "Ngôi nhà của yêu thương",
    27: "Băng tan",
    28: "Chuyến du lịch thú vị",
    29: "Lễ hội ở Nhật Bản",
    30: "Ngày hội",
}


def phan_loai(name):
    """Tra ve (tap, so_bai) de sap xep. File khong dung mau -> (9, 0)."""
    m = re.match(r"tap2-bai(\d+)_", name, re.I)
    if m:
        return 2, int(m.group(1))
    m = re.match(r"Bai_(\d+)_", name, re.I)
    if m:
        return 1, int(m.group(1))
    return 9, 0


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else FOLDER
    if not os.path.isdir(folder):
        print("Khong tim thay thu muc:", folder); sys.exit(1)

    files = [f for f in os.listdir(folder) if f.lower().endswith(".mp3")]
    files.sort(key=lambda f: (*phan_loai(f), f.lower()))

    names, codes, la = [], [], []
    tap_truoc = None
    for f in files:
        tap, so = phan_loai(f)
        if tap != tap_truoc:
            tieu_de = {1: "TIẾNG VIỆT 4 - TẬP 1", 2: "TIẾNG VIỆT 4 - TẬP 2"}.get(tap, "FILE KHAC")
            if codes:
                codes.append("")
            codes.append(tieu_de)
            tap_truoc = tap
        names.append(f)
        if tap == 1:
            label = f"Bài {so}: {TEN_TAP1[so]}" if so in TEN_TAP1 else f"Bài {so}"
        elif tap == 2:
            label = f"Tập 2 - Bài {so}: {TEN_TAP2[so]}" if so in TEN_TAP2 else f"Tập 2 - Bài {so}"
        else:
            label = os.path.splitext(f)[0]
            la.append(f)
        codes.append(f'[audio_task label="{label}" src="{CDN}/{SUBDIR}/{f}"]')

    with open(os.path.join(OUT_DIR, "ds_mp3_tieng_viet_4.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(names) + "\n")
    with open(os.path.join(OUT_DIR, "shortcode_tieng_viet_4.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(codes) + "\n")

    for f in names:
        print(f)
    n1 = sum(1 for f in names if phan_loai(f)[0] == 1)
    n2 = sum(1 for f in names if phan_loai(f)[0] == 2)
    print(f"\nTong {len(names)} file: Tap 1 = {n1}, Tap 2 = {n2}")

    thieu1 = [k for k in TEN_TAP1 if not any(phan_loai(f) == (1, k) for f in names)]
    thieu2 = [k for k in TEN_TAP2 if not any(phan_loai(f) == (2, k) for f in names)]
    if thieu1:
        print("  THIEU Tap 1, bai:", thieu1)
    if thieu2:
        print("  THIEU Tap 2, bai:", thieu2)
    if la:
        print("  File khong dung mau ten:", la)
    print("Da ghi ds_mp3_tieng_viet_4.txt va shortcode_tieng_viet_4.txt")


if __name__ == "__main__":
    main()