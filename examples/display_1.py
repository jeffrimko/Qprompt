from qprompt import alert, echo, error, warn
echo("Just a message.")
alert("Heads up!")
warn("Uh oh...")
error("OMG this is bad!")
error("REALLY BAD", end="!!!!!!!\n")
