title: weeknotes WK1
date: 07-08-2022
---

Inspired by other [weeknotes](https://simonwillison.net/tags/weeknotes/) and the
desire to capture the knowledge, thoughts, questions I encounter each week in a
place that is not exclusive to me. Week 1!

## Starting things & streaks

For the most part, I feel like a fairly disciplined individual and am well set
in my routines and habits. But there's lots of things I want to do, with little
time to fit it in. Trying to mash them in all at once is also difficult and the
wrong approach.

My oldest has been learning french in school and now that summer is here, I
thought it'd be fun to continue some of that learning. So, I downloaded
[Streaks](https://streaksapp.com/) for iOS and am on a 6 day Duolingo streak.
Nothing impressive, but I'm going to work my way towards some fun vocabulary
that him and I can share. Upside is that Duolingo Kids is a great product.

Hopefully once I get this as a habit (only 15 min a day of Duolingo!) I can
follow through with dedicating 30 minutes a day to my
[Gameboy emulator](https://github.com/bartek/zigboy). A little trickier due to the heavy
context you need to immerse yourself in, so we'll see.

And yes, I'm using that app to manage my `weeknotes` streak (starting today!)


## An introduction to AI-powered semantic search

This
[video](https://www.youtube.com/watch?v=7ozfzKLTFV4&list=PLq-odUc2x7i8eaYHVXSOadHrVE9tEU2QR)
was a great introduction into the world of semantic & supervised search, history
of the tooling, and the shift towards this "new paradigm". As someone who has
minimal experience in this space, I enjoyed this talk. Notes of interest:

* Traditional keyword search typically used when you have sparse document
  representations. An inverted index gets you quite far.

* New paradigm and the tooling around it is about retrieving documents using
  nearest neighbour search. BERT is big here. All the classic tools (like
  Elastic) are now supporting vector / nearest neighbour search, but not without
  problems.

* Supervised search is another technique. You need labelled data, and you give
  the machine those labelled examples. Common trap is to train with an
  inappropriate data set (flying a car to drive a train).

* [MS Marco](https://microsoft.github.io/msmarco/) is a huge data set from
  Microsoft (8.8m passages, 500k labelled). Real queries sampled from bing. It's
  very hard to get *good* labelled data

* When you don't have labelled data, BM25 is a good baseline and starting point.

## Go reflection and custom marshalling

At work, I encountered a fun Go problem where I need to marshal any arbitrary
struct into a JSON representation that modifies the JSON output at the field
level, while ensuring only specified fields from the struct are marshalled.

Basically, you go from something like this:

[sourcecode:go]
type Book struct {
   Author string `json:"author"`
   Title string `json:"title"`
   LastIndexed int `json:"last_indexed"`
}
[/sourcecode]

To this:

[sourcecode:json]
{
   "author": {
      "assign": "Kim Stanley Robison",
   },
   "title": {
      "assign": "Red Mars (Trilogy #1)"
   }
}
[/sourcecode]

Note the lack of `last_indexed` in the output. In this case, it is not a
writeable field. However, we do want it to be marshalled (and unmarshalled) in
other cases. 

At compile time, we know which fields can be assigned this operator (not all
fields can be marshalled this way). We know the types which we'd like to provide this custom marshalling, and we don't want to overload `MarshalJSON`.

The immediate idea was to implement a custom marshaler, but that overloads the
JSON tag. Not all fields should be in this output. We could use an auxiliary
struct though:

[sourcecode:go]
func (b Book) MarshalJSON() ([]byte, error) {
   return json.Marshal(&struct{
        Author string `json:"author"`
        Title string `json:"title"`
   }{
        Author: b.Author,
        Title: b.Title,
   })
}
[/sourcecode]

This overloads the marshaler which isn't great. We could of course have a
custom method, `MarshalJSONWritable()`. This works, but it gets cumbersome with
a lot of fields and many types. Now the behaviour for what is writeable is
sprinkled in many places, and can be worsened if there's particular behaviour
we'd need to implement for each marshaler. (I hinted with the `assign` key
that there may be more than one operator to consider)

So what next? I took inspiration from the `json` tag itself and pondered
implementing a custom struct tag. Struct tags are small pieces of metadata
attached to a struct which provides instructions to other parts of your Go code
as to how it should work with this struct. I can enrich the struct with a custom
tag, signalling that these are writeable.

[sourcecode:go]
type Book struct {
   Author string `json:"author" assign:"author"`
   Title string `json:"title" assign:"title"`
   LastIndexed int `json:"last_indexed"`
}
[/sourcecode]

I then wrote a simple function which uses reflect to find fields with this tag,
checking for a few additional traits, like `omitempty`. An example of that,
snipped for brevity:


[sourcecode:go]
func assignableFields(v any) map[string]any {
    keys := reflect.TypeOf(v)
    values := reflect.ValueOf(v)

    assignable := fields{}
    for i := 0; i < keys.NumField(); i++ {
            field := keys.Field(i)
            value := values.Field(i)
            tag := field.Tag.Get(assignTagName)

            // ... tag checks and omitempty snipped

            assignable[tag] = value.Interface()
    }

    return assignable
}
[/sourcecode]

The output is the assignable fields inside a `map[string]any` which can now be
marshalled as prescribed by the underlying types. With this, the behaviour around
the `assign` tag is in a single method (`assignableFields`) and I can package
all possible operators in one space. There's possibly a bit of digging to
understand what this `assign` tag is and where its behaviour is defined, but
that's something I will work through.

I found this solution to be more elegant than auxiliary structs and custom
marshalling but it might surprise me as it gets primed through use. We'll see!



## TIL

* Skip index: This came up in a chat about
  [ClickHouse](https://clickhouse.com/). In a traditional relational database,
  we create indexes and may create "secondary" indexes to a table to improve
  query performance, in particular, to reduce the possibility of table scans.
  ClickHouse isn't 1:1 with relational databases, so they introduce the concept
  of skip indexes. This different type of index enables ClickHouse to skip
  reading significant chunks of data that are guaranteed to have no matching
  values. More
  [here](https://clickhouse.com/docs/en/guides/improving-query-performance/skipping-indexes/)


## End

This was a long weeknotes and it's my first. I'm going to imagine future ones
will be less ambitious. Either way, this was fun.
