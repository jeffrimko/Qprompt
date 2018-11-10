from qprompt import alert, echo, error, warn, info
echo("Just a message.")
alert("Heads up!")
info("Hmm...")
warn("Uh oh...")
error("OMG this is bad!")
error("REALLY BAD", end="!!!!!!!\n")
