#! /usr/bin/env python

"""
統合テストを実行するときは、Postgresデータベースエンジンがすでにバックグラウンドで実行されている必要があります。
また、たとえば、元のデータベースを使用できるように構成されている必要があります。
さらに、すべてのテストが実行されたら、データベースを削除し、データベースエンジンを停止する必要があります。

これはDockerにとって完璧な仕事であり、最小限の構成で複雑なシステムを分離して実行できます。
"""


import os
import json
import subprocess
import time

import click
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# Ensure an environment variable exists and has a value
def setenv(variable, default):
    os.environ[variable] = os.getenv(variable, default)


APPLICATION_CONFIG_PATH = "config"
DOCKER_PATH = "docker"

# 一部のDockerコンテナ（まもなく使用するPostgreSQLコンテナなど）は、
# 初期設定を実行するために環境変数に依存しているため、
# 環境変数がまだ初期化されていない場合は、設定する関数を定義する必要があります。
# また、構成ファイルのパスをいくつか定義します。

def app_config_file(config):
    return os.path.join(APPLICATION_CONFIG_PATH, f"{config}.json")


def docker_compose_file(config):
    return os.path.join(DOCKER_PATH, f"{config}.yml")


def read_json_configuration(config):
    # Read configuration from the relative JSON file
    with open(app_config_file(config)) as f:
        config_data = json.load(f)

    # Convert the config into a usable Python dictionary
    config_data = dict((i["name"], i["value"]) for i in config_data)

    return config_data

# 原則として、少なくとも開発、テスト、本番環境では異なる構成を期待しているので、
# 導入しapp_config_file、docker_compose_file作業している環境の特定のファイルを返します。
# 関数read_json_configuration は configure_app、テストによってインポートされるため、分離されています。
# データベースリポジトリを初期化します。
def configure_app(config):
    configuration = read_json_configuration(config)

    for key, value in configuration.items():
        setenv(key, value)


@click.group()
def cli():
    pass


# これは、コンテナーをオーケストレーションする必要があるときはいつでも、
# オプションの長いリストを繰り返さないようにするDockerComposeコマンドラインを作成する単純な関数です。
def docker_compose_cmdline(commands_string=None):
    config = os.getenv("APPLICATION_CONFIG")
    configure_app(config)

    compose_file = docker_compose_file(config)

    if not os.path.isfile(compose_file):
        raise ValueError(f"The file {compose_file} does not exist")

    command_line = [
        "docker-compose",
        "-p",
        config,
        "-f",
        compose_file,
    ]

    if commands_string:
        command_line.extend(commands_string.split(" "))

    return command_line


# この関数をrun_sql使用すると、実行中のPostgresデータベースでSQLコマンドを実行でき、
# 空のテストデータベースを作成するときに役立ちます。
def run_sql(statements):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOSTNAME"),
        port=os.getenv("POSTGRES_PORT"),
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()


# Postgresコンテナーを監視し、使用する準備ができていることを確認する簡単な方法です。
# プログラムでコンテナを起動するときはいつでも、準備が整う前に特定の起動時間があることを認識し、それに応じて行動する必要があります。
def wait_for_logs(cmdline, message):
    logs = subprocess.check_output(cmdline)
    while message not in logs.decode("utf-8"):
        time.sleep(1)
        logs = subprocess.check_output(cmdline)



"""
この関数は、私たちが定義する最後の関数であり、管理スクリプトによって提供される唯一のコマンドです。まず、アプリケーションはという名前testingで構成されconfig/testing.jsonますdocker/testing.yml。これは、構成ファイルとDockerComposeファイルを使用することを意味します。これらの名前とパスはすべて、この管理スクリプトの任意の設定に由来する単なる規則であるため、プロジェクトを別の方法で自由に構成できます。

次に、この関数は、を実行しているDockerComposeファイルに従ってコンテナーを起動しdocker-compose up -dます。データベースが接続を受け入れる準備ができていることを通知するログメッセージを待機し、テストデータベースを作成するSQLコマンドを実行します。

この後、デフォルトのオプションセットを使用してPytestを実行し、コマンドラインで提供するすべてのオプションを追加し、最終的にDockerComposeコンテナーを破棄します。

セットアップを完了するには、DockerComposeの構成ファイルを定義する必要があります
"""
@cli.command()
@click.argument("args", nargs=-1)
def test(args):
    os.environ["APPLICATION_CONFIG"] = "testing"
    configure_app(os.getenv("APPLICATION_CONFIG"))

    cmdline = docker_compose_cmdline("up -d")
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("logs postgres")
    wait_for_logs(cmdline, "ready to accept connections")

    run_sql([f"CREATE DATABASE {os.getenv('APPLICATION_DB')}"])

    cmdline = [
        "pytest",
        "-svv",
        "--cov=application",
        "--cov-report=term-missing",
    ]
    cmdline.extend(args)
    subprocess.call(cmdline)

    cmdline = docker_compose_cmdline("down")
    subprocess.call(cmdline)


if __name__ == "__main__":
    cli()