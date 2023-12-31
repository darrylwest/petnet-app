#!/usr/bin/env python3
# dpw@plaza.localdomain
# 2023-09-09 14:26:17

import sys
import os
from rich import print, inspect
import httpx

# from petnet_app import

import time

from faker import Faker

fake = Faker()
verbose = False
port = 9001  # TODO(dpw): get from common config
host = f"http://127.0.0.1:{port}"


def create_headers():
    return {
        "Content-type": "application/json; charset=utf-8",
        "accept": "application/json; charset=utf-8",
    }


def test_home():
    url = f"{host}/"
    print(f"test_home() {url}")
    response = httpx.get(url)

    if response.status_code != 200:
        print(f"text: {response.text}, status code: {response.status_code}")
        if verbose:
            inspect(response)

    assert response.status_code == 200
    if verbose:
        inspect(response)


def test_ping():
    url = f"{host}/api/ping"
    print(f"test_ping() {url}")
    response = httpx.get(url, headers=create_headers())

    if response.status_code != 200:
        print(f"text: {response.text}, status code: {response.status_code}")
        if verbose:
            inspect(response)

    assert response.status_code == 200
    if verbose:
        inspect(response)

    assert "pong" in response.text


def test_info():
    url = f"{host}/api/info"
    print(f"test_info() {url}")
    response = httpx.get(url, headers=create_headers())

    if response.status_code != 200:
        print(f"text: {response.text}, status code: {response.status_code}")
        if verbose:
            inspect(response)

    assert response.status_code == 200
    if verbose:
        inspect(response)

    info = response.json()
    assert int(info.get("pid", 0)) > 0


def main(args: list) -> None:
    print(f"{args}")

    test_home()
    test_ping()
    test_info()


if __name__ == "__main__":
    args = sys.argv[1:]

    # parse sub-commands here
    if "--verbose" in args:
        verbose = True

    main(args)
