# Wait for a port to be listening in Salt
pubdate: 2016-03-23 19:22:20 +0100
tags: Salt

Sometimes, you want to wait for a service to be running before running other
states. Usually this can be done with a `service.running` state, which is then
required by other states. For example, a `mysql_database.present` state can
require the mysql service state, and it won't be ran before the mysql service
has been started.

However, sometimes the service can start up but still not be ready to serve
requests. I faced this problem with InfluxDB - there would be up to a 1 second
delay between `service influxdb start` and InfluxDB actually listening on all
the ports. Because of this, `influxdb_user.present` states would fail if the
service had been restarted due to configuration changes, because the connection
to port 8086 would fail.

The solution: Using `until` and `nc`/`netcat`.

```
influxdb:
  pkg.installed: []
  service.running:
    - name: influxdb
  cmd.run:
    - name: until nc -z localhost 8086; do sleep 1; done
    - timeout: 10
    - onchanges:
      - service: influxdb

influxdb-user-example:
  influxdb_user.present:
    - name: example
    - passwd: example
    - require:
      - cmd: influxdb
```

What's happening here is that whenever the service gets restarted, that counts
as a change in the `service.running` state. That triggers the `cmd.run` state,
which will be executed synchronosusly - in other words, it'll block other states
from being executed until it completes. Then, our states that require the port
to be listening simply add a requirement for the `cmd.run` state.

In Salt 2016.3, you don't even need the `cmd:` in front of the requirement.
