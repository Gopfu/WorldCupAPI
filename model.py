# -*- coding:utf-8 -*-

import copy
import datetime
from peewee import Model, CharField, DateTimeField, SqliteDatabase, IntegerField

db = SqliteDatabase("worldcup1.db")


class BaseModel(Model):
    """数据库模块基类"""

    class Meta:
        database = db

    @classmethod
    def get_one(cls, *query, **kwargs):
        # 查询不到返回None，而且不抛异常
        try:
            return cls.get(*query, **kwargs)
        except Exception:
            return None

    def get_dict(self, ignore=None):
        '''
        :param ignore 忽略不返回的字段，list列表输入
        return 字典类型
        '''
        data = copy.copy(self.__dict__.get('_data'))
        if ignore and isinstance(ignore, list):
            for ign in ignore:
                if data.has_key(ign):
                    del data[ign]
        return data


class Group(BaseModel):
    """
    32强

    name: 组名
    group: 组别
    team：队名
    """
    name = CharField(null=True)
    group = CharField(null=True)
    team = CharField(null=True)

    class Meta:
        db_table = 'world_cup_group'


class Points(BaseModel):
    """
    积分榜

    group: 组别
    team: 队名
    team_order: 小组排名
    count: 场次
    goal: 进球数
    lose_goal: 失球数
    true_goal: 净进球数
    score: 积分
    lose: 负场
    win: 胜场
    draw: 平场
    """
    group = CharField(null=True)
    team = CharField(null=True)
    team_order = IntegerField(null=True)
    count = IntegerField(null=True)
    goal = IntegerField(null=True)
    true_goal = IntegerField(null=True)
    lose_goal = IntegerField(null=True)
    score = IntegerField(null=True)
    lose = IntegerField(null=True)
    win = IntegerField(null=True)
    draw = IntegerField(null=True)

    class Meta:
        db_table = 'world_cup_points'


class Matches(BaseModel):
    """
    赛程

    group: 组别
    team1: 左边队名
    score1: 左边队积分
    team2: 右边队名
    score2: 右边队积分
    city: 比赛城市
    status: 比赛状态，1未进行，2进行中，3结束
    date: 比赛时间
    """
    group = CharField(null=True)
    team1 = CharField(null=True)
    score1 = IntegerField(null=True)
    team2 = CharField(null=True)
    score2 = IntegerField(null=True)
    city = CharField(null=True)
    status = IntegerField(null=True)
    date = DateTimeField(null=True, formats='%Y-%m-%d %H:%M')

    class Meta:
        db_table = 'world_cup_matches'


if __name__ == '__main__':
    db.create_tables([Group, Points, Matches], safe=True)
