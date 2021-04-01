def getLittleEndianNumber(arr):
    return int.from_bytes(arr, "little")


class Chunk:
    """
    表示一个 RIFF CHUNK

    """
    id = ""  # 块标志，4个ASCII字符组成，用以识别块中所包含的数据。如：'RIFF','LIST','fmt','data','WAV','AVI'等等
    length = 0  # 块大小，四字节无符号整型，小端字节序 => 指示 data 的长度
    data = bytes()  # 块数据

    def __init__(self, arr):
        self.id = arr[:4]
        self.length = getLittleEndianNumber(arr[4:8])
        self.data = arr[8:8 + self.length]

    def totalLen(self):
        """
        返回这个Chunk占用的总空间
        :return:
        """
        return 8 + self.length


class IdxEntry:
    """
    表示一个 RIFF 索引条目
    """
    id = ""
    flags = ""
    offset = 0
    length = 0

    def __init__(self, arr):
        self.id = arr[:4]
        self.flags = arr[4:8]
        self.offset = getLittleEndianNumber(arr[8:12])
        self.length = getLittleEndianNumber(arr[12:16])

    @staticmethod
    def totalLen():
        return 16


class RIFF:
    id = ""  # List块标志
    size = 0  # 块大小，四字节无符号整型，小端字节序 => 指示 type 和 data 的长度
    type = ""  # 块类型，4个ASCII字符组成，用以识别块中所包含的数据。如：'RIFF','LIST','fmt','data','WAV','AVI'等等
    data = []  # List块数据，包含若干个 Chunk

    def __init__(self, videoFile):
        # 读取整个文件
        file = open(videoFile, "rb")
        self.id = file.read(4)
        self.size = getLittleEndianNumber(file.read(4))
        self.type = file.read(4)
        self.data = file.read(self.size - 4)
        file.close()

    @staticmethod
    def measureChunk(arr):
        s = getLittleEndianNumber(arr[4:8])
        return s + 8

    @staticmethod
    def measureList(arr):
        s = getLittleEndianNumber(arr[4:8])
        return s + 8

    def getMovieEntry(self, need):
        """
        获取 RIFF AVI 的 movi 部分，包括 need 中指定的帧类型
        :param need     例如：[b'00dc', b'01wb']
        :return:
        """
        cur, total = 0, self.size - 4
        chunks = []
        while cur < total:
            _id = self.data[cur: cur + 4]
            if _id == b"LIST":
                t = self.data[cur + 8: cur + 12]
                if t == b"movi":
                    # 提取视频流
                    size = getLittleEndianNumber(self.data[cur + 4: cur + 8])
                    cur += 12
                    end = cur + size - 4
                    while cur < end:
                        # 有时候视频块和音频块之间会多一个 0x00，感觉是用来填充的，解析的时候这边进行跳过
                        if self.data[cur] == 0:
                            cur += 1
                        _id = self.data[cur:cur + 4]
                        if _id in need:
                            c = Chunk(self.data[cur:])
                            cur += c.totalLen()
                            chunks.append(c)
                            pass
                        else:
                            cur += RIFF.measureChunk(self.data[cur:])
                    pass
                else:
                    cur += RIFF.measureList(self.data[cur:])
            else:
                cur += RIFF.measureChunk(self.data[cur:])
        return chunks

    def getRawVideoEntry(self):
        """
        获取 RIFF AVI 的 movi 部分，H.264 编码的视频流（不包括音频流）
        :return:
        """
        return self.getMovieEntry([b"00dc"])

    def getAllMovieEntry(self):
        """
        获取 RIFF AVI 的 movi 部分，包括视频流和音频流
        :return:
        """
        return self.getMovieEntry([b"00dc", b"01wb"])

    def getIdx(self):
        """
        获取 RIFF AVI 的索引内容
        :return: 索引数组
        """
        cur, total = 0, self.size - 4
        chunks = []
        while cur < total:
            _id = self.data[cur: cur + 4]
            if _id == b"LIST":
                cur += RIFF.measureList(self.data[cur:])
            elif _id == b"idx1":
                cur += 8
                while cur < len(self.data):
                    idx = IdxEntry(self.data[cur:])
                    cur += idx.totalLen()
                    chunks.append(idx)
            else:
                cur += RIFF.measureChunk(self.data[cur:])
        return chunks


class Fragment:
    """
    表示一个碎片
    """
    entries = []  # 里面存放 IdxEntry 或者 Chunk


class Movie:
    """
    表示一个视频，包含碎片和索引
    """
    fragments = []  # 存放碎片列表
    idx = []  # 存放视频索引

    def getPositionInIndex(self, fragment: Fragment) -> int:
        """
        获取某个碎片，在索引表中的起始位置，如果没有找到，则返回-1
        :param fragment:
        :return:
        """
        verifyLen = 0
        for i in range(len(self.idx)):
            # if self.idx[i].length == fragment.entries[verifyLen]
            pass

        return verifyLen == len(fragment.entries)

    def generateGraph(self):
        """
        根据当前知道的视频的碎片信息和索引信息，生成一个有向无权图
        :return:
        """
        pass


class Node:
    """
    表示一个图的节点，每个节点包含一个碎片
    """
    fragment = Fragment()  # 存放碎片


class Edge:
    """
    表示一个图的有向边，包含权重和起止点
    """
    start = Fragment()  # 起始节点
    end = Fragment()  # 目的节点
    weight = 0  # 边权重


class Graph:
    """
    表示一个有向图，包含一组节点和边
    """
    nodes = []  # 存放所有的节点
    edges = []  # 存放所有的边
