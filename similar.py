# coding:utf-8
import pandas as pd
import fire


def check_similar(s1, s2):
    """比较两个字符串的相似度
    :param s1: string 字符串1
    :param s2: string 字符串2
    :return: float 返回相似度
    """
    if s1 is None:
        return
    if s2 is None:
        return
    s1 = set(list(s1))
    s2 = set(list(s2))
    return len(s1 & s2) / len(s1 | s2)


def find_similar(df, threshold=0.8, id_col_num=0, name_col_num=3):
    """找出文档中的符合相似度的字符串
    :param df： pd.DataFrame 包含字符串的文档
    :param threshold： float 相似度
    :param id_col_num： int 参考列号
    :param name_col_num： int 需要对比字符串的列号
    :return list: 返回包含符合相似度的结果列表
    """
    result = []
    for i in range(len(df)):
        _id1 = df.iloc[i, id_col_num]
        name1 = df.iloc[i, name_col_num]
        s1 = set(list(name1))
        for j in range(i + 1, len(df)):
            _id2 = df.iloc[j, id_col_num]
            name2 = df.iloc[j, name_col_num]
            s2 = set(list(name2))

            if check_similar(s1, s2) >= threshold:
                info1 = {'ref': _id1,
                         'similar_str': name1
                         }
                result.append(info1)
                info2 = {'ref': _id2,
                         'similar_str': name2
                         }
                result.append(info2)
    return result


def main(target_path, save_path, id_col_num, name_col_num):
    """主函数，运行命令行程序
    :param target_path：str 目标路径
    :param save_path: str 保存路径
    :param id_col_num： int 参考列号
    :param name_col_num： int 需要对比字符串的列号 
    """
    df = pd.read_excel(target_path)
    result = find_similar(df, id_col_num=id_col_num, name_col_num=name_col_num)
    out = pd.DataFrame(result)
    out.to_csv(save_path, index=False)


if __name__ == '__main__':
    fire.Fire(main)
