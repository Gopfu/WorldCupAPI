# -*- coding:utf-8 -*-
# Author      : Binfu
# Created     : 2018/06/28
# Description : 世界杯赛况API

import json
from flask import Flask, jsonify, request
from peewee import fn
from model import Group, Points, Matches

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def index():
    return "World Cup information API."


@app.route('/groups')
def get_groups():
    """
    获取32强组
    """
    page = int(request.args.get('page', 1))
    pre_page = int(request.args.get('pre_page', 4))
    groups = Group.select().paginate(page, pre_page)
    data = [g.get_dict() for g in groups]
    return json_data(data)


@app.route('/truegoals')
def get_true_goals():
    """
    获取每个小组净胜球最大的队伍
    """
    teams = Points.select(Points.group, Points.team, fn.Max(Points.true_goal)).where(
        Points.team == Points.team).group_by(Points.group)
    data = [g.get_dict() for g in teams]
    return json_data(data)


@app.route('/scorediff')
def get_score_diff():
    """
    获取比分差最大的三场比赛
    """
    matches = Matches.select()
    # SQL查询目前不清楚怎么做，先用其他方法处理
    matches_diff = {m.id: abs(m.score1 - m.score2) for m in matches}
    sort = sorted(matches_diff.items(), key=lambda x: x[1], reverse=True)[:3]
    sort = sorted(sort, reverse=True)
    data = [Matches.get_one(id=s[0]).get_dict() for s in sort]
    # matches = Matches.select(Matches.id, fn.Max(Matches.score1 - Matches.score2)).group_by(
    #     Matches.group).limit(3).order_by(-Matches.date)
    return json_data(data)


@app.route('/advance')
def get_advance():
    """
    获取每个小组晋级的队伍
    """
    teams = Points.select().where(Points.team_order << [1, 2])
    data = [Points.get_one(id=t.id).get_dict() for t in teams]
    return json_data(data)


def json_data(data, message="", code=0):
    """
    返回json格式数据
    data: 返回数据
    message: 信息
    code: 状态码
    """
    data_dict = {}
    data_dict["data"] = data
    data_dict["message"] = message
    data_dict["code"] = code
    return jsonify(data_dict)
    # return json.dumps(data_dict, ensure_ascii=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
