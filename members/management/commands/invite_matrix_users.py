import sys
from contextlib import redirect_stdout
from io import StringIO

import matrix_commander
from django.conf import settings
from django.core.management.base import BaseCommand

from members.models import get_intern_matrix_members


def call_matrix_commander(*args):
    return matrix_commander.main([
        "matrix-commander",
        "-s", "matrix_client_store",
        "-c", "matrix_client_store/credentials.json",
        *args,
    ])


def matrix_login():
    call_matrix_commander(
        "--homeserver", "https://matrix.org",
        "--user-login", settings.MATRIX_USERNAME,
        "--password", settings.MATRIX_PASSWORD,
        "--login", "password",
        "--device", "device",
        "--room-default", settings.MATRIX_ROOM_NAME,
    )


def matrix_invite(handles):
    for matrix_handle in handles:
        call_matrix_commander("--room-invite", settings.MATRIX_ROOM_NAME, "--user", matrix_handle)


def matrix_kick(handles):
    for matrix_handle in handles:
        call_matrix_commander("--room-kick", settings.MATRIX_ROOM_NAME, "--user", matrix_handle)


def get_channel_members():
    with redirect_stdout(StringIO()) as buffer:
        call_matrix_commander("--joined-members", settings.MATRIX_ROOM_ID)
    current_members_output = buffer.getvalue()
    current_members_output = [m.strip().partition(" ")[0] for m in current_members_output.splitlines()]
    return set(
        m
        for m in current_members_output
        if m.startswith("@")
    )


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not settings.MATRIX_ROOM_ID or not settings.MATRIX_ROOM_NAME or not settings.MATRIX_USERNAME or not settings.MATRIX_PASSWORD:
            print("Missing MATRIX_* config, check settings and try again.")
            sys.exit(1)

        matrix_login()

        members_should = set(get_intern_matrix_members().values_list("contactinfo__matrix_handle", flat=True))
        members_should.add("@metalab_room_inviter_bot:matrix.org")
        members_should.add("@metalab_room_owner_bot:matrix.org")
        members_is = get_channel_members()

        members_kick = (members_is - members_should)
        members_invite = (members_should - members_is)

        print(f"inviting: {members_invite}")
        matrix_invite(members_invite)
        print(f"kicking: {members_kick}")
        matrix_kick(members_kick)
