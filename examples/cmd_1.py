import qprompt
while True:
    cmd = qprompt.ask_str("command", vld=["help", "run", "quit"], blk=False)
    if "help" == cmd:
        print("DO HELP")
    if "run" == cmd:
        print("DO RUN")
    if "quit" == cmd:
        exit()
