# coding:utf-8
import pandas as pd
import fire

def check_similar(s1, s2):
    '''
        param: s1,s2 string
            ratio float
        return float
    '''
    if s1 is None:
        return
    if s2 is None:
        return
    s1 = set(list(s1))
    s2 = set(list(s2))
    return len(s1 & s2) / len(s1 | s2)


def find_similar(df, threshold=0.8, id_col_num=0, name_col_num=3):
    '''
        param: df pd.DataFrame
                threshold float
        return list
    '''
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
                info1 = {'InstitutionID': _id1,
                         'InstitutionName': name1
                         }
                result.append(info1)
                info2 = {'InstitutionID': _id2,
                         'InstitutionName': name2
                         }
                result.append(info2)
    return result


def main(target_path, save_path, id_col_num, name_col_num):
    # path = r"F:\steven\Documents\WXWork Files\File\2018-11\华东宁波医药无经纬度机构20181126.xlsx"
    df = pd.read_excel(target_path)
    result = find_similar(df, id_col_num=id_col_num, name_col_num=name_col_num)
    out = pd.DataFrame(result)
    out.to_csv(save_path, index=False)


if __name__ == '__main__':
    fire.Fire(main)
