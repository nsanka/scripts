import twisted.internet.asyncioreactor
twisted.internet.asyncioreactor.install()
from twisted.internet import reactor, task
import ipywidgets, datetime, subprocess, functools, os

class DoneError(Exception):
    pass

def time_out_counter(reactor):
    label = ipywidgets.Label("Time left: 5:00")
    current_seconds = datetime.timedelta(minutes=5).total_seconds()
    def decrement(count):
        nonlocal current_seconds
        current_seconds -= count
        time_left = datetime.timedelta(seconds=max(current_seconds, 0))
        minutes, left = divmod(time_left, minute)
        seconds = int(left.total_seconds())
        label.value = f"Time left: {minutes}:{seconds:02}"
        if current_seconds < 0:
            raise DoneError("finished")
    minute = datetime.timedelta(minutes=1)
    call = task.LoopingCall.withCount(decrement)
    call.reactor = reactor
    d = call.start(1)
    d.addErrback(lambda f: f.trap(DoneError))
    return d, label

def editor(fname):
    textarea = ipywidgets.Textarea(continuous_update=False)
    textarea.rows = 20
    output = ipywidgets.Output()
    runner = functools.partial(subprocess.run, capture_output=True, text=True, check=True)
    def save(_ignored):
        with output:
            with open(fname, "w") as fpout:
                fpout.write(textarea.value)
            print("Sending...", end='')
            try:
                runner(["git", "add", fname])
                runner(["git", "commit", "-m", f"updated {fname}"])
                runner(["git", "push"])
            except subprocess.CalledProcessError as exc:
                print("Could not send")
                print(exc.stdout)
                print(exc.stderr)
            else:
                 print("Done")
    textarea.observe(save, names="value")
    return textarea, output, save

def journal():
    date = str(datetime.date.today())
    title = f"Log: Startdate {date}"
    filename = os.path.join(f"{date}.txt")
    d, clock = time_out_counter(reactor)
    textarea, output, save = editor(filename)
    box = ipywidgets.VBox([
        ipywidgets.Label(title),
        textarea,
        clock,
        output
    ])
    d.addCallback(save)
    return box

journal()