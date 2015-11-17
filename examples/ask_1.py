import qprompt
name = qprompt.ask_str("Name", blk=False)
age = qprompt.ask_int("Age", vld=range(130))
if qprompt.ask_yesno("Say hello?", dft="y"):
    print "Hi %s! You are %u years old!" % (name, age)
    qprompt.pause()
