title: Using Go's Context and WaitGroups to gracefully handle goroutines
date: 02-15-2021

---

Recently I was building a application that would tick on an interval and on each tick,
produce potentially thousands of goroutines. I wanted to ensure when the application was terminated, it would exit gracefully and quickly, even if particular goroutines were processing slowly.

Initially, I was using `sync.WaitGroup` to control flow, primarily around how I log
output, but I quickly realized that if I created many goroutines and even a small
collection of them did not return immediately, my application would hang when being
terminated. This led me to reviewing `context.WithCancel` and understanding how I can
adjust my application to be well suited for quick and graceful termination!

We can demonstrate this by building up from an application which, initially, does not use
either: 

[sourcecode:go]
    package main

    import (
            "fmt"
            "log"
            "math/rand"
            "os"
            "os/signal"
            "syscall"
            "time"
    )

    func doSomething(ch chan int) {
            fmt.Printf("Received job %d\n", <-ch)
    }

    func init() {
            rand.Seed(time.Now().Unix())
    }

    func main() {
            var (
                    closing   = make(chan struct{})
                    ticker    = time.NewTicker(1 * time.Second)
                    logger    = log.New(os.Stderr, "", log.LstdFlags)
                    batchSize = 6
                    jobs      = make(chan int, batchSize)
            )

            go func() {
                    signals := make(chan os.Signal, 1)
                    signal.Notify(signals, syscall.SIGTERM, os.Interrupt)
                    <-signals
                    close(closing)
            }()
    loop:
            for {
                    select {
                    case <-closing:
                            break loop
                    case <-ticker.C:
                            for n := 0; n < batchSize; n++ {
                                    jobs <- n
                                    go doSomething(jobs)
                            }
                            logger.Printf("Completed doing %d things.", batchSize)
                    }
            }
    }
[/sourcecode]

When the program is run, we observe the sequence of _"Received job ..."_ messages alongside the completion message (_"Completed doing .."_). It might look something like this:

    Received job 0
    Received job 1
    Received job 2
    2021/02/08 21:30:59 Completed doing 6 things.
    Received job 3
    Received job 4
    Received job 5
    2021/02/08 21:31:00 Completed doing 6 things.

The results don't print consistently! This makes sense as we know that goroutines are not
blocking so unless we do somethign about it, code after them will execute immediately. We can add a
`WaitGroup` to improve flow. First, define it in the `var` block:

    [sourcecode:go]
    var (
        ..
        wg sync.WaitGroup
    )
    [/sourcecode]

Adjust the loop:

    [sourcecode:go]
    for n := 0; n < batchSize; n++ {
        wg.Add(1)
        jobs <- n
        go doSomething(&wg, jobs)
    }
    wg.Wait()
    logger.Printf("Completed doing %d things.", batchSize)
    [/sourcecode]

And finally, the goroutine:

    [sourcecode:go]
    func doSomething(wg *sync.WaitGroup, ch chan int) {
        defer wg.Done()
        fmt.Printf("Received job %d\n", <-ch)
    }
    [/sourcecode]

[WaitGroups](https://golang.org/pkg/sync/#WaitGroup) wait for a collection of
goroutines to finish. If we read the code out loud, we can see that:

1. On each iteration of the loop, we add `1` to the WaitGroup. We add `1`
   because our goroutine will call `wg.Done()` once, which decrements the
   WaitGroup counter by one. It balances out as each goroutine returns.
2. Before the `logger` call, we add `wg.Wait()`. This tells our Go program to block
   until the WaitGroup counter is zero. The counter will be zero when all
   goroutines have called `wg.Done()`

Simple, right? If we run the program again we can see the results print more
consistently:

    2021/02/08 21:46:47 Completed doing 6 things.
    Received job 0
    Received job 1
    Received job 2
    Received job 4
    Received job 5
    Received job 3
    2021/02/08 21:46:48 Completed doing 6 things.
    Received job 0
    Received job 2
    Received job 3
    Received job 4
    Received job 5
    Received job 1

By the way, it's expected the jobs won't be ordered! We haven't done anything to
ensure that.

Before we continue, run the application as it is thus far and try to terminate it,
usually this is done by hitting `Control-d`. The program should exit without issue.

To demonstrate further need for control, let's add a piece of code that's more akin to a real-world
scenario. We'll make a new function which calls out to an API and expects a response.
We'll then use `context.WithCancel` to cancel the request while it's in flight.

First, create the new function without any context. It's going to be heavier,
so follow the in-line commentary as necessary:

    [sourcecode:go]
    func doAPICall(wg *sync.WaitGroup) error {
            defer wg.Done()

            req, err := http.NewRequest("GET", "https://httpstat.us/200", nil)
            if err != nil {
                    return err
            }

            // The httpstat.us API accepts a sleep parameter which sleeps the request for the
            // passed time in ms
            q := req.URL.Query()
            sleepMin := 1000
            sleepMax := 4000
            q.Set("sleep", fmt.Sprintf("%d", rand.Intn(sleepMax-sleepMin)+sleepMin))
            req.URL.RawQuery = q.Encode()

            // Make the request to the API in an anonymous function, using a channel to
            // communicate the results
            c := make(chan error, 1)
            go func() {
                    // For the purposes of this example, we're not doing anything with the response.
                    _, err := http.DefaultClient.Do(req)
                    c <- err
            }()

            // Block until the channel is populated
            return <-c
    }
    [/sourcecode]

Modify the ticker interval; remove the previous call to `doSomething`, optionally drop the
`jobs` channel (we won't use it further), and add a call to `doAPICall`:

    [sourcecode:go]
    for n := 0; n < batchSize; n++ {
        wg.Add(1)
        go doAPICall(&wg)
    }
    [/sourcecode]

Run the application and try to exit again.

* The WaitGroup continues to wait until all go routines are finished. 
* The `doAPICall` function blocks until a response is returned from the `httpstat.us` API, and that can
  range anywhere from `1000` to `4000` ms.
* Depending on when you try to terminate the application, it can be difficult to do so (you may
  not notice this on first pass, run it a few times and try to terminate at different
  times)

Now to demonstrate how `context.WithCancel` provides further control over program cancellation. When `context.WithCancel` is initialised, it provides a context and a `CancelFunc`. This cancel func can cancel the context, which sounds confusing at first pass; Reading [Go Concurrency Patterns: Context](https://blog.golang.org/context) from The Go Blog helped, and I recommend checking that out after this post!

Ok, back to it. There's little that needs to be done to the application to have it support this
cancellation flow. First, create a new context with cancellation function:

    [sourcecode:go]
    var (
        ctx, cancel = context.WithCancel(context.Background())
        ...
    )
    [/sourcecode]

Then, in the anonymous function where we watch for program termination, call the `CancelFunc` after
the `signals` channel is notified. This means that the context will be considered cancelled:

    [sourcecode:go]
    go func() {
            signals := make(chan os.Signal, 1)
            signal.Notify(signals, syscall.SIGTERM, os.Interrupt)
            <-signals
            logger.Println("Initiating shutdown of producer.")
            cancel()
            close(closing)
    }()
    [/sourcecode]

Then, adjust the `doAPICall` function to accept a context, and modify the return statement
to use a blocking `select`, waiting on either the `ctx.Done` channel or the request
response. Parts of the function snipped for brevity:

    [sourcecode:go]
    func doAPICall(ctx context.Context, ....) {
        // Cancel the request if ctx.Done is closed or await the response
        select {
        case <-ctx.Done():
            return ctx.Err()
        case err := <-c:
            return err
        }
    }
    [/sourcecode]

Finally, ensure the call to `doAPICall` has been adjusted to pass the context. Now, run
the application and terminate it at different start times.

What happens now? The application terminates immediately. The blocking `select` call
watches for the closure of `ctx.Done` or the response on `c`, whichever comes first. When
the application is terminated, `ctx.Done` takes precedence and the function returns early,
not concerning itself with the response of the request. The WaitGroup continues to do its
specific job and the flow of the application during termination is much improved!

There's many ways this can be expanded or used, so please consider it a starting point. I
initially struggled understanding how I could use `WaitGroup` and `context.WithCancel` in
combination, so I hope this was useful!

For reference, here's the code in its entirety:

    [sourcecode:go]
    package main

    import (
            "context"
            "fmt"
            "log"
            "math/rand"
            "net/http"
            "os"
            "os/signal"
            "sync"
            "syscall"
            "time"
    )

    func doAPICall(ctx context.Context, wg *sync.WaitGroup) error {
            defer wg.Done()

            req, err := http.NewRequest("GET", "https://httpstat.us/200", nil)
            if err != nil {
                    return err
            }

            // The httpstat.us API accepts a sleep parameter which sleeps the request for the
            // passed time in ms
            q := req.URL.Query()
            sleepMin := 1000
            sleepMax := 4000
            q.Set("sleep", fmt.Sprintf("%d", rand.Intn(sleepMax-sleepMin)+sleepMin))
            req.URL.RawQuery = q.Encode()

            c := make(chan error, 1)
            go func() {
                    // For the purposes of this example, we're not doing anything with the response.
                    _, err := http.DefaultClient.Do(req)
                    c <- err
            }()

            // Block until either channel is populated or closed
            select {
            case <-ctx.Done():
                    return ctx.Err()
            case err := <-c:
                    return err
            }
    }

    func init() {
            rand.Seed(time.Now().Unix())
    }

    func main() {
            var (
                    closing     = make(chan struct{})
                    ticker      = time.NewTicker(1 * time.Second)
                    logger      = log.New(os.Stderr, "", log.LstdFlags)
                    batchSize   = 6
                    wg          sync.WaitGroup
                    ctx, cancel = context.WithCancel(context.Background())
            )

            go func() {
                    signals := make(chan os.Signal, 1)
                    signal.Notify(signals, syscall.SIGTERM, os.Interrupt)
                    <-signals
                    cancel()
                    close(closing)
            }()
    loop:
            for {
                    select {
                    case <-closing:
                            break loop
                    case <-ticker.C:
                            for n := 0; n < batchSize; n++ {
                                    wg.Add(1)
                                    go doAPICall(ctx, &wg)
                            }
                            wg.Wait()
                            logger.Printf("Completed doing %d things.", batchSize)
                    }
            }
    }
    [/sourcecode]


As a final note, a portion of this code was inspired by the [Go Concurrency Patterns:
Context](https://blog.golang.org/context) blog post, which I, again, recommend. It
introduces further controls like `context.WithTimeout` and well, the Go blog is a treasure that everyone should read!
