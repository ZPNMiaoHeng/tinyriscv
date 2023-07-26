import glob, os, logging, re, fnmatch

# 配置日志输出格式
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")

# 查找rtl
## 打印目标文件
def print_files(fileType):
    print("Found {} tinyriscv files".format(len(fileType)))
    for file in fileType:
        print(file)
    print()

## 查找文件并输出相关打印信息
def printFiles(findFilePath, fileType, verbose=False):
    findFile = glob.glob(os.path.join(findFilePath, "*.{}".format(fileType)))
    if verbose:
        print_files(findFile)
    return findFile

corePath = os.path.join("..", "rtl", "core" )
debugPath = os.path.join("..", "rtl", "debug" )
peripsPath = os.path.join("..", "rtl", "perips" )
socPath = os.path.join("..", "rtl", "soc" )
utilPath = os.path.join("..", "rtl", "utils" )

ysyxFiles  = printFiles(corePath  , "v", False)# True)
ysyxFiles += printFiles(debugPath , "v", False)# True)
ysyxFiles += printFiles(peripsPath, "v", False)# True)
ysyxFiles += printFiles(socPath   , "v", False)# True)
ysyxFiles += printFiles(utilPath  , "v", False)# True)
# print_files(ysyxFiles)

defineFiles = ["../rtl/core/defines.v"]
# print_files(defineFiles)

ysyxFiles = set(ysyxFiles) - set(defineFiles) 
# print_files(ysyxFiles)

# 合并文件
with open("./build/ysyx_tinyriscv.v", "w") as log:
    # log.write("/* verilator lint_off DECLFILENAME */\n")
    # log.write("/* verilator lint_off UNUSEDPARAM */\n")
    # log.write("/* verilator lint_off UNUSEDSIGNAL */\n")
    # log.write("/* verilator lint_off REDEFMACRO */\n")
    # log.write("`define RISCV_FORMAL\n")  # add tracing
    # log.write("`define RVFI\n")  # add tracing

    for path in defineFiles:
        filename = os.path.basename(path)
        with open(path) as f:
            content = f.read()
            log.write(content)
            # print("merge define" + path)
    logging.info("merge define Files")

    for path in ysyxFiles:
        filename = os.path.basename(path)
        with open(path) as f:
            content = f.read()
            content = re.sub(r"^\s*(`include)\s+.*\n", "", content, flags=re.MULTILINE)
            log.write(content)
            # print("merge v" + path)
    logging.info("merge v Files")
