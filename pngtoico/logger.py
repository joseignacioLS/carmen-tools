class Logger:
    def __init__(self, file):
        self.file = file
        self.reset()

    def reset(self):
        open(self.file, "w")

    def log(self, msg, label):
        with open(self.file, "a") as inputF:
            inputF.write(f"{label}: {msg}\n")
