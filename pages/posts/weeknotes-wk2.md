title: weeknotes WK2
date: 07-15-2022
---

## Streaks continued

As mentioned last week, I downloaded [Streaks](https://streaksapp.com/) for iOS
in order to get myself into new habits. These notes and Duolingo specifically.

Duolingo was hit and miss. I streaked for 5 days only to miss a day, then got
back, and then missed another day. I've been allotting the evening for Duolingo
time, and I believe that's most appropriate based on my schedule, but the kids
can be exhausting (our youngest decided to have some bad nights after a few
very good weeks of sleep)

At least I am here for week two :)

## Go reflection and custom marshalling

As a follow up to [last weeks](../weeknotes-wk1) thinking, the solution I ended up was quite similar
to what was described. However, I ended up using a dependency! Turns out much of
what I was attempting to accomplish, which can be summarized by converting an
arbitrary `any` struct to `map[string]interface{}` in order to further massage
the data is handled by [github.com/fatih/structs](https://github.com/fatih/structs).

Fatih is well known in the Go community, and although this project is read-only,
it is stable, well tested, and does more extensively what I was already doing
with reflect.

Mildly validating to see that others faced such a problem and built tooling to
support it. The library handles the custom struct tag issue as well, which is
great!

## Reading

* [Build: An Unorthodox Guide to Making Things Worth Making](https://www.goodreads.com/book/show/59696349-build). I've now been working at a startup for 8 months and the mentality, energy, drive, and potential for burn around the space is really meshing with what I want right now. I'm getting excited about what we're building, but also getting excited to build more myself. The book begins with highlights from the story of [General Magic](https://www.justwatch.com/ca/movie/general-magic), which was one of those mystical (and anti-pattern filled) startups creating something seemingly revolutionary that ultimately, was not a desirable product for anyone but the engineers who were making it.

* [Why is life expectancy in the US lower than in other rich
  countries?](https://ourworldindata.org/us-life-expectancy-low) was a widely
  shared blog post from the Our World in Data team. Frustrating to see that many
  of the most preventable deaths (homicide, opiod overdose, and road accidents)
  can be preventable with the right supports. Inequality of course, makes a
  showing.

## TIL

* `Monotonically` is a new word for me. In simplest terms, this means something
  that goes up or stalls, but never goes down. For example, the number of people
  born this year is increasing monotonically. Once someone is born, they cannot
  be unborn. Conversely, world population or birth rates are not monotonic.
  Although usually going up, it may go down. With [birth rates
  decreasing](https://ourworldindata.org/grapher/crude-birth-rate), maybe the
  world population may hit a down slope in the coming decades?


