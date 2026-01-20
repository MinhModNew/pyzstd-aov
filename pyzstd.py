import getopt
import os
import sys
try:
	import pyzstd
	import colorama
except:
	os.system('pip install pyzstd')
	os.system('pip install colorama')
	import pyzstd
	import colorama
	os.system("cls")

hentaiz = open("Code/dict.bytes", 'rb')
ZSTD_DICT = hentaiz.read()
ZSTD_LEVEL = 17

def usage() -> None:
    print("\nUsage:\n\t{} [option] <file 1 path> <file 2 path> ...".format(sys.argv[0]))
    print("option:")
    print("\t-h, --help\t\tShow this")
    print("\t-c, --compress\t\tCompress Zstd")
    print("\t-d, --decompress\tDecompress Zstd")

def main() -> None:
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hcd", ["help", "compress", "decompress"])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
    
    if not args:
        args = (input(" 📂 Nhập Thư Mục: "), )

    args = set(args)
    for input_path in list(args):
        if os.path.isdir(input_path):
            args.discard(input_path)
            
            for entry in os.scandir(input_path):
                if entry.is_file():
                    args.add(entry.path)

    for input_path in args:
        input_blob = None
        try:
            with open(input_path, "rb") as f:
                input_blob = f.read()
        except FileNotFoundError:
            print("\n❌Lỗi!! Không Thể Tìm Thấy Thư Mục \"{}\"!!!  ".format(input_path))
            continue

        if b'"Jg' in input_blob:
            continue            

        if opts:
            opt, arg = opts[0]
        else:
            pos = input_blob.find(b"\x28\xb5\x2f\xfd")
            if pos != -1:
               opt = "-d"
               input_blob = input_blob[pos:]
            else:
                opt = "-c"
        
        zstd_mode = None
        try:
            if opt in ("-c", "--compress"):
                zstd_mode = "mã hoá"
                output_blob = bytearray(pyzstd.compress(input_blob, ZSTD_LEVEL, pyzstd.ZstdDict(ZSTD_DICT, True)))

                output_blob[0:0] = len(input_blob).to_bytes(4, byteorder="little", signed=False)
                output_blob[0:0] = b"\x22\x4a\x00\xef"
            elif opt in ("-d", "--decompress"):
                input_blob = input_blob[input_blob.find(b"\x28\xb5\x2f\xfd"):]

                zstd_mode = "giải mã"
                output_blob = pyzstd.decompress(input_blob, pyzstd.ZstdDict(ZSTD_DICT, True))

            output_path = input_path
            with open(output_path, "wb") as output_file:
                output_file.write(output_blob)
        except pyzstd.ZstdError:
            print("\n❌Bị Lỗi {} \"{}\" Xong!!".format(zstd_mode, input_path))
            continue
        print("\n✅File Được {} \"{}\" Xong!!! ".format(zstd_mode, input_path))
    
    print("\nĐã Hoàn Thành!!")

if __name__ == "__main__":
    while True:
        main()
