import pandas as pd


class StructureMerger:
    def __init__(self, filepath1: str, filepath2: str):
        dataFrame1 = pd.read_csv(filepath1)
        dataFrame2 = pd.read_csv(filepath2)
        dict1 = {}
        dict2 = {}
        # 把表里的数据读入集合，进行下一步的操作，添加一个"#"符号用来区分Source和Target值
        for i in range(len(dataFrame1)):
            dict1[str(dataFrame1["Source"][i]) + "#" + str(dataFrame1["Target"][i])] = \
                dataFrame1["Weight"][i]
        for i in range(len(dataFrame2)):
            dict2[str(dataFrame2["Source"][i]) + "#" + str(dataFrame2["Target"][i])] = \
                dataFrame2["Weight"][i]
        self.dict1 = dict1
        self.dict2 = dict2
        # 枚举合并时候可能出现的情况
        self.TABLE1_ONLY = 0
        self.TABLE2_ONLY = 1
        self.TABLE_BOTH = 2

    def _innerMerge(self, keySet: set, flag: int, source: list, target: list, weight: list, dataType: list):

        if flag == self.TABLE1_ONLY:
            for item in keySet:
                inner_ls = item.split("#")
                source.append(inner_ls[0])
                target.append(inner_ls[1])
                weight.append(self.dict1[item])
                dataType.append("表1独有")
        elif flag == self.TABLE2_ONLY:
            for item in keySet:
                inner_ls = item.split("#")
                source.append(inner_ls[0])
                target.append(inner_ls[1])
                weight.append(self.dict2[item])
                dataType.append("表2独有")
        elif flag == self.TABLE_BOTH:
            for item in keySet:
                inner_ls = item.split("#")
                source.append(inner_ls[0])
                target.append(inner_ls[1])
                weight.append((self.dict1[item] + self.dict2[item]) / 2)
                dataType.append("表1表2共有")

    def merge(self):
        source = []
        target = []
        weight = []
        dataType = []
        # 情况1，数据只存在于表1
        self._innerMerge(set(self.dict1.keys()) - set(self.dict2.keys()), self.TABLE1_ONLY, source, target, weight,
                         dataType)
        # 情况2，数据只存在于表2
        self._innerMerge(set(self.dict2.keys()) - set(self.dict1.keys()), self.TABLE2_ONLY, source, target, weight,
                         dataType)
        # 情况3，数据既存在于表1又存在于表2
        self._innerMerge(set(self.dict1.keys()) & set(self.dict2.keys()), self.TABLE_BOTH, source, target, weight,
                         dataType)

        df = pd.DataFrame([source, target, weight, dataType]).T

        df.columns = ["Source", "Target", "Weight", "Belong"]

        df.to_excel("合并结果.xlsx", index=False)


if __name__ == '__main__':
    merger = StructureMerger("edge2015_1(1).csv", "edge2015_2(1).csv")
    merger.merge()
