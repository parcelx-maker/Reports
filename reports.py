#!/usr/bin/python
# -*- coding: UTF-8 -*-
from module import Report
import pymysql
from settings import PARCELX_DB_HOST, PARCELX_DB_PWD, PARCELX_DB_PORT, PARCELX_DB_USER
# import datetime
from datetime import datetime, timezone, timedelta
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
        print("开始生成统计表")
        today = datetime.utcnow().replace(tzinfo=timezone.utc)
        yesterday = today - timedelta(days=1)
        today = today.strftime('%Y-%m-%d')
        yesterday = yesterday.strftime('%Y-%m-%d')
        hour = '11:00:00.000000'
        # 北京时间19点，UTC11点
        sql = "SELECT account_info.`name`, parcel_track.parcel_no, parcel_track.`status`, parcel_track.create_time FROM parcel_track INNER JOIN parcel_info ON parcel_track.parcel_no = parcel_info.parcel_no INNER JOIN account_info ON account_info.id = parcel_info.account_no WHERE parcel_track.create_time > '{} {}' AND parcel_track.create_time < '{} {}' ".format(
            yesterday, hour, today, hour)
        print(sql)
        db = pymysql.connect(host=PARCELX_DB_HOST, user=PARCELX_DB_USER, passwd=PARCELX_DB_PWD, port=PARCELX_DB_PORT,
                             db='parcelx', charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()

        self.title = "Parcel tracking record daily statistics report {} to {}".format(yesterday, today)
        self.msg = "包裹跟踪记录统计表每日报告 UTC {} {} 至 {} {}".format(yesterday, hour, today, hour)

        track_dict = dict()

        for item in data:
            if item[0] in track_dict:
                if item[1] in track_dict[item[0]]:
                    if track_dict[item[0]][item[1]]['create_time'] < item[3]:
                        track_dict[item[0]][item[1]] = {"status": item[2], "create_time": item[3]}
                else:
                    track_dict[item[0]][item[1]] = {"status": item[2], "create_time": item[3]}
            else:
                track_dict[item[0]] = {item[1]: {"status": item[2], "create_time": item[3]}}
        db.close()

        report_dict = dict()
        for account in track_dict:
            if account not in report_dict:
                report_dict[account] = dict()
            for parcel_no in track_dict[account]:
                parcel_status = track_dict[account][parcel_no]['status']
                if parcel_status not in report_dict[account]:
                    report_dict[account][parcel_status] = 1
                else:
                    report_dict[account][parcel_status] += 1
        book = xlwt.Workbook()
        sheet = book.add_sheet('sheet1')
        sheet.write(0, 0, "UTC {} {} 到 UTC {} {} 包裹追踪统计".format(yesterday, hour, today, hour))
        sheet.write(1, 0, "日期")
        sheet.write(1, 1, "客户名称")
        i = 2
        for status in self.PARCEL_STATUS:
            sheet.write(1, i, self.PARCEL_STATUS[status])
            i += 1
        c = 2
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
        self.attaches.append(self.title + '.xls')


if __name__ == '__main__':
    ptd = ParcelTrackDaily()
    ptd.generate()
    ptd.send()
