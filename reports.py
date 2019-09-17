#!/usr/bin/python
# -*- coding: UTF-8 -*-
from module import Report
import pymysql
from settings import PARCELX_DB_HOST, PARCELX_DB_PWD, PARCELX_DB_PORT, PARCELX_DB_USER
import datetime
import xlwt


class ParcelTrackDaily(Report):
    PARCEL_STATUS = {
        0: "未知",
        3: "已下单",
        1001: "已拣货",
        1002: "已发货",
        2001: "已起运",
        2004: "已着陆",
        3001: "已提货",
        3003: "开始清关",
        3005: "清关结束",
        4003: "在途",
        4005: "已签收",
        9001: "电商确认完成",
    }

    def generate(self):
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        sql = "SELECT account_name,`status`,COUNT(parcel_no) FROM parcel_track WHERE create_time > '{} 19:00:00.000000' AND create_time < '{} 19:00:00.000000' GROUP BY `status`  ORDER BY account_no".format(
            str(yesterday), str(today))
        db = pymysql.connect(host=PARCELX_DB_HOST, user=PARCELX_DB_USER, passwd=PARCELX_DB_PWD, port=PARCELX_DB_PORT,
                             db='parcelx', charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()

        self.title = "每日包裹跟踪记录统计表 {} - {}".format(str(yesterday), str(today))
        self.msg = "见附件"
        report_dict = dict()

        for item in data:
            if item[0] not in report_dict:
                report_dict[item[0]] = {item[1]: item[2]}
            else:
                report_dict[item[0]][item[1]] = item[2]

        db.close()

        book = xlwt.Workbook()
        sheet = book.add_sheet('sheet1')
        sheet.write(0, 0, "日期")
        sheet.write(0, 1, "客户名称")
        i = 2
        for status in self.PARCEL_STATUS:
            sheet.write(0, i, self.PARCEL_STATUS[status])
            i += 1
        c = 1
        for client in report_dict:
            sheet.write(c, 0, str(today))
            sheet.write(c, 1, client)
            i = 2
            for status in self.PARCEL_STATUS:
                for s in report_dict[client]:
                    if s == str(status):
                        sheet.write(c, i, report_dict[client][s])
                i += 1
            c += 1
        book.save(self.title + '.xls')


if __name__ == '__main__':
    ptd = ParcelTrackDaily()
    ptd.generate()
    ptd.send()
