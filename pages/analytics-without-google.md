title: Analytics without Google
date: 06-02-2020
---

Last week, I launched a [personal project](https://freethedocs.app). A nice change
that most definitely came from a desire to *do something else* during covid-19
lockdown. With that launch came a desire to have some level of analytics, I
didn't need the full customer journey but I sure was curious how many people
were using my site after I submitted it to Hacker News y'know?

I was also motivated to continue to de-Google my life, something
I've been doing with [email](https://fastmail.com),
[hosting](https://digitalocean.com), and [search](https://duckduckgo.com).

So my little service was running, but analytics! I could grep my `nginx`
log files to get a gauge, but I wanted something more robust. I discovered a
paid service named [Simple Analytics](https://simpleanalytics.com) which offers
privacy-focused analytics that, as the name suggests, are simple.

This was great, but not ideal for me. My application was not generating any
revenue (nor did it have intention to), so I needed something else. For the
record, I do recommend checking them out. 

So what was ideal for me?

* _Essential_ analytics. I wasn't after knowing the full customer
    journey, I was just curious how many people were hitting my service over
    time.
* Free and ideally open source.
* Not invasive to privacy. I don't want to track my users with cookies or sessions.
* Built-in interaction with standard *nix log formats and plays nicely with log
    rotation.
* Light weight and compilable by me. Ideally I can self-host this and don't have
    to worry about piping my data to another service.

## Enter GoAccess

Immediately, this seemed to meet my primary criteria, with further consideration
for tracking more interesting metrics like application response times. So, I
gave [GoAccess](https://goaccess.io/) a try. Installation was trivial and with a simple command, I had output:

    ./goaccess /var/log/nginx/access.log

GoAccess plays nicely with Apache and nginx log formats, although it supports a
large variety. This command opens up a Terminal-based visualization of various
panels of data for your server.

This was great and there's even support for HTML based static and real-time
dashboards. The output of which is beautiful:

![HTML Based Dashboard](/static/analytics-google/goaccess-dashboard.png)

(My humble blog and service don't get much traffic, that's OK)

An immediate concern I had was that my logs would rotate. By default when you
install `nginx`, a `logrotate` configuration is added to rotate them daily.
Luckily, GoAccess makes it easy to analyse over multiple files:

    ./goaccess /var/log/nginx/access.log /var/log/nginx/access.log.1
    /var/log/nginx/access.log.2

But this would get frustrating to write and adjust on each rotation. Luckily, we
can leverage the pipe operator. I love how composable unix applications are!

    zcat /var/log/nginx/access.log.*.gz | ./goccess /var/log/nginx/access.log -

The result took a few dozen more milliseconds compared to parsing a single
access file but was otherwise the same experience when browsing the data. Just
more information!

![GoAccess Multiple Logs](/static/analytics-google/goaccess-multilog.png)

Of course, because of the platform we're on (Linux!), we can compose the data
our application will capture in various ways. For example, assuming I rotated logs on a daily basis and wanted 
the last 15 days of log files (including today):

    zcat /var/log/nginx/access.log.{1..15}.gz | ./goccess /var/log/nginx/access.log -

So this was nice. It gave me plenty of what I wanted and I liked the various
output options. Leveraging the operating system, I can use other tools to
specify what kind of data I want parsed and GoAccess treats it all the same.

## Giving it a go

I scoured the web for a few more options, finding a few others like
[GoatCounter](https://www.goatcounter.com/) but it didn't match my full
criteria (in this case, it isn't self-hosted).

What I further liked about GoAccess is I could run it on a separate machine, transferring
logs from multiple servers into one place, then creating my necessary
dashboards. This plays nicely with the fact that I'm running Digital Ocean
Droplet's, which although don't go kaboom on their own, I make a tendency myself
to erase and start from scratch (just testing my resiliency in re-provisioning
servers)

GoAccess reminded me how beautiful composable tools like it are. Its feature set is
minimal and it plays nicely with the tools already available to us on a *nix
platform. Do one thing and do it well -- words of wisdom.
