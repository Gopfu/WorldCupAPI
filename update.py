# -*- coding:utf-8 -*-
# Author      : Binfu
# Created     : 2018/06/28
# Description : 更新世界杯比赛和积分信息

import os
import json
import time
import datetime
import requests
from bs4 import BeautifulSoup
from model import Group, Points, Matches, db


GROUP_URL = "http://2018.sina.com.cn/teams/"
POINTS_URL = ("http://api.sports.sina.com.cn/?p=sports&s=sport_client&a=index&_sport_t_=football&"
    "_sport_s_=opta&_sport_a_=teamOrder&type=108&use_type=group")
MATCHES_URL = ("http://api.sports.sina.com.cn/?p=sports&s=sport_client&a=index&_sport_t_=livecast"
    "&_sport_a_=groupMatchesByType&type=108&limit=100&season=2017&dpc=1")


def get_groups():
    """
    获取32强组名和组别
    """
    print("Get or update World Cup groups.")
    group = Group().get_one()
    if not group:
        html = requests.get(GROUP_URL).content
        soup = BeautifulSoup(html)
        for group in soup.select(".-live-page-widget"):
            group_list = group.get_text().split()
            if not group_list:
                continue
            name = group_list[0]
            for team in group_list[1:]:
                char = [t for t in name][0]
                group = "%s%s" % (char, group_list.index(team))
                Group.create(name=name, group=group, team=team)


def get_points():
    """
    获取积分榜接口
    """
    print("Get or update World Cup points.")
    html = requests.get(POINTS_URL).content
    group_points = json.loads(html)
    for teams in group_points["result"]["data"].values():
        for team in teams:
            point = Points.get_one(team=team.get("team_cn"))
            if point and point.count == int(team.get("count", 0)):
                continue
            if not point:
                Points.create(
                    group=team.get("group"),
                    team=team.get("team_cn"),
                    team_order=team.get("team_order"),
                    count=team.get("count"),
                    goal=team.get("goal"),
                    true_goal=team.get("truegoal"),
                    lose_goal=team.get("losegoal"),
                    score=team.get("score"),
                    lose=team.get("lose"),
                    win=team.get("win"),
                    draw=team.get("draw")
                )
            else:
                Points.update(
                    team_order=team.get("team_order"),
                    count=team.get("count"),
                    goal=team.get("goal"),
                    true_goal=team.get("truegoal"),
                    lose_goal=team.get("losegoal"),
                    score=team.get("score"),
                    lose=team.get("lose"),
                    win=team.get("win"),
                    draw=team.get("draw")
                ).where(Points.id == point.id).execute()


def get_match():
    """
    获取比赛信息
    """
    print("Get or update World Cup matches.")
    html = requests.get(MATCHES_URL).content
    group_points = json.loads(html)
    for group in group_points["result"]["data"]:
        match = Matches.get_one(team1=group.get("Team1"), team2=group.get("Team2"))
        if match and match.status == 3:
            continue
        date = "%s %s" % (group.get("date"), group.get("time"))
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        if not match:
            score1 = group.get("Score1") if group.get("Score1") else None
            score2 = group.get("Score2") if group.get("Score2") else None
            Matches.create(
                group=group.get("group"),
                team1=group.get("Team1"),
                score1=score1,
                team2=group.get("Team2"),
                score2=score2,
                city=group.get("MatchCity"),
                status=int(group.get("status")),
                date=date,
            )
        else:
            match.scor1 = group.get("Score1")
            match.scor2 = group.get("Score2")
            match.status = int(group.get("status"))
            match.save()


def update(internal=30):
    """
    更新赛况赛程信息

    internal: 间隔时间，默认30分钟更新一次
    """
    if not os.path.isfile("worldcup.db"):
        db.create_tables([Group, Points, Matches], safe=True)
    while True:
        get_groups()
        get_points()
        get_match()
        time.sleep(internal * 60)


if __name__ == '__main__':
    update()
