#!/bin/bash

# set -e : コマンドのreturn_codeが0以外だったら終了
# set -x : デバッグログを表示
set -ex

# このスクリプトの絶対パス
SCRIPT_DIR=$(cd $(dirname $0); pwd)

# プロジェクトルートの絶対パス
ROOT_DIR=$(cd $(dirname $0)/..; pwd)

cd $ROOT_DIR

# SQLiteデータベースファイルを削除
rm -f $ROOT_DIR/mydatabase.db

# マイグレーション
alembic upgrade head

# 初期ユーザー作成
PASSWD="admin"
python api/manage.py create-user sys_admin -r SYSTEM_ADMIN -p $PASSWD
python api/manage.py create-user loc_admin -r LOCATION_ADMIN -p $PASSWD
python api/manage.py create-user loc_operator -r LOCATION_OPERATOR -p $PASSWD