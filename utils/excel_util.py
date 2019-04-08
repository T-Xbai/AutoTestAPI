# -- coding: utf-8 --
from openpyxl import load_workbook


class ExcelUtil:
    """
     Excel 文件操作工具类
    """

    _wb = None

    def __init__(self, filename: str):
        self._wb = load_workbook(filename=filename)

    def getTitleIndex(self):
        """
        获取标题对应的坐标顺序
        :return: title value 与 title index
        """
        _SHEET_NAME = 'Template'
        title_index = {}
        for sheet in self.sheets():
            if sheet.title == _SHEET_NAME:
                for row in sheet.rows:
                    for cell in row:
                        title_index[cell.value] = cell.col_idx - 1
                return title_index
        raise Exception("没有找到工作溥名称为 : %s ,请到文件中添加 " % _SHEET_NAME)

    def getConfig(self):
        """
        获取工作溥配置
        """

        _SHEET_NAME = 'Config'
        config = {}
        for sheet in self.sheets():
            if sheet.title == _SHEET_NAME:
                for row in sheet.rows:
                    key = row[0].value
                    conf_value = row[1].value
                    config[key] = conf_value
                return config
        raise Exception("没有找到工作溥名称为 : %s ,请到文件中添加 " % _SHEET_NAME)

    def sheets(self):
        """
        获取工作溥集合
        """
        return self._wb.worksheets

    def sheet(self, name):
        for sheet in self.sheets():
            if sheet.title == name:
                return sheet
        raise Exception("没有找到工作溥名称为 : %s " % name)

    def rows(self, sheet):
        return sheet.rows

    def cell(self, sheet, r_col, c_col):
        return sheet.cell(row=r_col, column=c_col)


if __name__ == '__main__':
    excel = ExcelUtil('../test_data/登录接口_test.xlsx')
    value = excel.getConfig()
    print(value)
