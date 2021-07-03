# Streaming and saving subprocess output at the same time in Python
pubdate: 2018-04-13 21:18 +0200
tags: Python

Sometimes, you want to run a subprocess with Python and stream/print its output
live to the calling process' terminal, and at the same time save the output to a
variable. Here's how:

```python
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
for line in proc.stdout:
    sys.stdout.buffer.write(line)
    sys.stdout.buffer.flush()
    # do stuff with the line variable here
proc.wait()
```
