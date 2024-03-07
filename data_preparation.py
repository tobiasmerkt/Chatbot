import re  # for data cleaning
import pandas as pd

### Clean Whatsapp chat ###

# open Whatsapp chat as downloaded in app
with open("original_chat.txt", "r") as f:
    original_chat = f.readlines()
# remove first information line about data encryption
original_chat = original_chat[1:]

# Remove the smiley in Vilianas name
chat = [line.replace("Viliana ❤️", "Viliana") for line in original_chat]

# remove placeholder for media such as voice messages, images, documents, ...
# u200e is unicode character for the LRM symbol which Whatsapp uses
chat = [re.sub(r"(Tobi|Viliana): \u200e.* weggelassen", "", line) for line in chat]
chat = [line for line in chat if "Dokument weggelassen" not in line]

# save the new chat
with open("clean_chat_with_ts.txt", "w", encoding="utf-8") as cleaned_file:
    cleaned_file.writelines(chat)

### Create DataFrame ###

# Regular expression to match the pattern in each line of the chat
pattern = r"\[(\d{2}\.\d{2}\.\d{2}, \d{2}:\d{2}:\d{2})] (.*?): (.*)"

times = []
names = []
messages = []

with open("clean_chat_with_ts.txt", "r", encoding="utf-8") as file:
    for line in file:
        match = re.match(pattern, line)
        if match:
            # Extract time, name, and message from each line
            times.append(match.group(1))
            names.append(match.group(2))
            messages.append(match.group(3))

# Create DataFrame
df = pd.DataFrame({"time": times, "name": names, "message": messages})
df["time"] = pd.to_datetime(df["time"], format="%d.%m.%y, %H:%M:%S")
df.insert(1, "time_diff", df["time"].diff())
df.loc[0, "time_diff"] = pd.Timedelta(seconds=0)
df["Group_nr"] = [0 for _ in range(len(times))]