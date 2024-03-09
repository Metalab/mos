# Things

MOS allows admins to maintain a list of Things (=devices, machines, permissions, ...)
and attach uses to them, e.g. user "ripper" is allowed to use thing "laser".
Additionally, things may report being used, e.g. "ripper" used "laser" for 60
seconds.

## Auth

Most endpoints require authentication. Ask Vorstand for a token and provide it
in the `X-TOKEN` header.

## Getting key IDs allowed to operate a Thing

```
$ curl https://metalab.at/things/keys/prusaxl -H "X-TOKEN: XXX"
00-000000000001,luto
00-000000000002,ripper
```

## Reporting usage of a thing

```
$ curl https://metalab.at/things/usage/prusaxl -H "X-TOKEN: XXX" -XPOST -d 'user=luto&kind=LOGIN'
```

`user` is a mos user/member, identified by their name, see `/keys/` endpoint.

`kind` may be:

* `LOGIN`, user started using a machine
* `LOGOUT`, user stopped using a machine
* `USAGE_MEMBER`, user used the machine for X seconds, for a member
* `USAGE_NONMEMBER`, user used the machine for X seconds, for a non-member
* `USAGE_METALAB`, user used the machine for X seconds, for a metalab infra project

Additionally, supply `usage_seconds=` as an integer for `USAGE_` kinds.

## Getting stats for a Thing

```
$ curl https://metalab.at/things/stats/laser
[["2024-02-24", 1], ["2024-02-24", 1]]
```

Format: `[[date of usage, usage in seconds],...]`.
