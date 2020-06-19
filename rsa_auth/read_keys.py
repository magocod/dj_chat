from datetime import datetime, timedelta, timezone

import jwt

private_key = ""
public_key = ""

with open("rsa-private.key", "r") as privatefile:
    # print(privatefile)
    lines = privatefile.readlines()
    length = len(lines)
    for index, line in enumerate(lines):
        # print(line)
        if index == 0:
            private_key = private_key + f"\n{line}"
            continue

        if index == length:
            private_key = private_key + f"\n{line}"
            continue

        private_key = private_key + line

print(private_key)

with open("rsa-public.key", "r") as publicfile:
    # print(publicfile)
    lines = publicfile.readlines()
    length = len(lines)
    for index, line in enumerate(lines):
        # print(line)
        if index == 0:
            public_key = public_key + f"\n{line}"
            continue

        if index == length:
            public_key = public_key + f"\n{line}"
            continue

        public_key = public_key + line

print(public_key)

delta_days = timedelta(days=365)
clain_day = datetime.now()
expired_time = clain_day + delta_days
timestamp = expired_time.replace(tzinfo=timezone.utc).timestamp()

print(clain_day)
print(expired_time)
print("timestamp", timestamp)
print(datetime.fromtimestamp(timestamp))

encoded = jwt.encode(
    {"exp": timestamp, "some": "payload"}, private_key, algorithm="RS256"
)
print("jwt", encoded)
decoded = jwt.decode(encoded, public_key, algorithms="RS256")
print("decoded", decoded)
