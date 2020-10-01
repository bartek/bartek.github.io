title: The Good Parts of AWS
date: 09-30-2020

---

This page is primarily a compilation of material from the book with the same
title, [The Good Parts of AWS](https://gumroad.com/l/aws-good-parts).

I wanted to compile this for myself. Having spent much of my career working with
*nix enviornments that I can SSH into and have full control over, I became quite
comfortable in managing such servers and navigating my way through `iptables`,
`nginx`, and more!

Then AWS came along and it all felt like a black box to me. This post is a
summary of the knowledge I've obtained thus far and should continue to grow over
time. It is incomplete, but figured I'd push what I have so far.

## DynamoDB

* Compared to relational databases, DynamoDB requires you to do most of the data
    querying within your application. If you want to aggregate, filter, or sort,
    you have to do that yourself, after you receive the requested data range.
    This characteristic will be one of the most important aspects of determining
    whether DynamoDB is a viable choice for your needs.
* Storage can get expensive, but generally the deciding factor comes to down
    request pricing.
* Start with on-demand pricing before considering provisioned capacity


## S3

* If you're storing data -- whatever it is -- S3 should be the very first thing
    to consider.
* Think of it as a highly durable hash table.
* It's cheap to store a lot. $23.55/TB/month using the default storage class.
* While storage costs are cheap, request pricing can be expensive.
* Consider who is touching your S3 files. Humans or computers? When the latter,
    request pricing becomes an important aspect of S3's viability for your use
    case.
* Bucket names are unique globally. Common mitigation is to always add your AWS
    acocunt ID to the bucket name.
* Buckets can be open, so you may find yourself uploading to someone elses
    bucket! Thankfully there's an API to check if you own the bucket, but watch
    out for this easy slip up!

## EC2

* Allows you to get a complete computer in the cloud in a matter of seconds.
* If you can run it on your computer, you can likely run it on EC2. You don't
    have to adapt your application to your host (for the most part).
* Most consequential decision you'll have to make is selecting an instance type
    (256 different types at time of writing)
* Can pay for time of instance or reserve instances for 1- or 3-year
    committments in exchange for reduced pricing.
* Spot instances are another cost saving option where you save by allowing EC2
    to take away your instance whenever it wants. Some use cases can handle
    this!
* Network security is daunting. Defaults are reasonable starting point. You'll
    need to look into the security group and the VPC ACL.

## EC2 Auto Scaling

* Amazon sells you this, but it's been rarely seen used successfully.
* Ask yourself if your EC2 costs are high enough that any reduction in usage
    will be materially significant? If your EC2 bill would go down by 30% --
    would that be a big deal for your business? If not, the effort and
    complexity of getting Auto Scaling working properly is likely not going to
    be worth it.
* If fluctuations are not significant or abrupt, not smooth, auto scaling will
    almost certainly not work well for you.
* There are secondary features which can't be ignored. The ability for an
    instance to be automatically replaced when unhealthy. The other benefit is
    how easy it is to update desired capacity, you get a dial that you can turn
    up and down!

## Lambda

* Abstract everything away into a function interface. Take input, produce output
    (or side effects)
* Consider Lambda when code should be part of the infrastructure (not the
    application)
* Lambda lets you hook into your application and introduce new capabilities. For
    example, S3 doesn't come with an API to resize an image after uploading, but
    this is a good use for Lambda.
* Keep it small. Lambda's risks will reveal themselves as the complexity of your
    application (or, function) grows
* Limitations may go away with time and they should be noted. Cold starts,
    limits to code bundle, network bandwidth.
* There are limitations inherent to how Lambda works which likely won't go away.

## ELB

* Comes in three variants, only two we need to care about for non-legacy
    software: Application (ALB), and Network (NLB), and Classic (legacy)
* ALBs are proper reverse proxies which sit between the internet and your
    application.
* NLBs behave like load balancers, but they work by routing network packets
    rather than by proxying HTTP requests. An NLB is more like a very
    sophisticated network router.
* Both do not validate cerficiates. Amazon provides this as a built-in, however
    remember that Amazon is now a man-in-the-middle itself. Amazon will be
    decrypting your network traffic and re-encrypting it when forwarding it to
    your application.

## CloudFormation

* You almost always want to use it (or a similar tool). Heavy initial investment
    that can pay off.
* Define resources as a YAML script (JSON also supported but less common), then
    you point CloudFormation to your Amazon account and it creates all the
    resources you defined.
* It is idempotent. Multiple runs won't do anything unless they have to.
* Careful to modify services controlled by CloudFormation manually.
    Unpredictable behaviour will ensue!
* Recommendation is to let CloudFormation deal with all the AWS things that are
    either static or change very rarely; such as VPC configurations, security
    groups, load balancers, deployment pipelines, and IAM roles.

## RDS

* Provides on demand databases and supports all major platforms (MySQL,
    PostgreSQL, Oracle)
* Ensure right-sizing of instances is considered. High cost to run an instance
    that is unnecessary. Heavy monitoring and iterative modification will yield
    cost savings.
* Provisioned IOPS provide a predictable, reliable amount of I/O but again can
    be costly.
* Just like EC2 has reduced pricing through reserved instances 

## Elasticache

* Caching-as-a-service running Memcached or Redis protocol-compliant server
    nodes.
* More or less twice as expensive for on-demand but prices drop quite quickly
    when looking at reserved instances.


## Appendix

### Provisioned Capacity

Significant cost savings with an upfront payment

### On-demand (Spot) Pricing

Low capacity management burden, higher costs

### Compute

AWS represents the computing power of its machines in Elastic Compute Units, and
4 ECUs represent more or less the power of a modern CPU.

## Resources

* [The Good Parts of AWS](https://gumroad.com/l/aws-good-parts?recommended_by=search)
* [ec2instances.info](https://www.ec2instances.info/)
* [AWS costs every programmer should know](https://david-codes.hatanian.com/2019/06/09/aws-costs-every-programmer-should-now.html)

