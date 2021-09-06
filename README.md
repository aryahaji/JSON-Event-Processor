
# Table of Contents
1. [Problem](README.md#problem)
2. [Instructions](README.md#instructions)
3. [Input Dataset](README.md#input-dataset)
4. [Output](README.md#output)
5. [Tips on rocking this code challenge](README.md#tips-on-rocking-this-code-challenge)
# First, Welcome!<br>
Hello :wave: and welcome to Webflow's DATE coding challenge! First off, we thank you for spending time with us, and we appreciate your interest in working here. Second, let us tell you about why we even have this screener in the first place.<br>
#### Why the screener?**<br>
You're here, which means we saw potential in your resume either through previous work experience, side projects, or other accomplishments/conversations. Congratulations! :blush:

# Problem

The DATE team at Webflow has just received a request to process events generated from our customers' hosted websites.  The information in one of these events can be useful in producing one or multiple new events with the use of some transformation logic. The Data Science team has requested that an event is produced for their consumption so that they can perform analysis and feed the information to their machine learning models.

For this exercise you are asked to process, transform and enrich the incoming events and produce new events as per requirements given by the data team.  The details on the input, processing and output can be found in the corresponding sections below.

*Disclosure: The projects that the DATE team is working on are much more complicated and interesting than this coding challenge. This challenge only tests you on the basics.*

# Instructions

We designed this coding challenge to assess your coding skills and your understanding of computer science fundamentals. To solve this challenge you might pick any of the following programming languages:  Java, Python, node.js or Scala. Whichever programming language you choose, you are only allowed to use the default data structures that come with that programming language (you might use I/O, testing and json libraries). For example, you can code in Python, but you should not use Pandas or any other external libraries.

***The objective here is to see if you can implement the solution using basic data structure building blocks and software engineering best practices (by writing clean, modular, and well-tested code).*** 

### Repo directory structure

The directory structure for your repo should look like this:

    ├── README.md 
    ├── api.spec.yaml 
    ├── src
    │   └── <your code should go in this folder>
    ├── input
    │   └── events.jsonlines
    |   └── event_schema.json
    ├── output
        └── analytics_events.jsonlines


### Steps to submit your solution

1. Create a branch of main for your solution
2. Submit a Pull Request.
3. Once you've submitted the pull request, one of the engineers on the team will go back-and-forth with you on the PR and perform a code review.

If you have any questions about this take-home, feel free to open an issue on the repository, and Gil or an engineer on the team will respond! Alternatively, feel free to forward any questions to your recruiter.

Anything that isn’t specifically specified in this project is up to your discretion. If you choose to make an assumption, document it and proceed. If you choose to omit something for the sake of time, again, document it and proceed.

Finally, we want to be respectful of your time. Our hope is that you spend no more than two hours on this project. If you find that you’ve invested all the time you can, then stop where you are and write things up. We are more interested in learning how you think about a problem and communicate technical details than the amount of code you can churn out. How you explain the remaining work and possible issues is just as important as whether you completed everything.

**Thank you for considering Webflow!** 💞

# Input Dataset

To simplify the exercise we will not be asking you to read and write from actual event streams. Instead you will use an input file (`events.jsonlines`) to represent the incoming event stream; within this file each row represents a discrete event. You can find the event schema in the  `event_schema.jsonschema` file within the input folder in the repo.

# Output 
Your solution needs to create the output file, `analytics_events.jsonlines` within the output folder in the repo. Each line of the file should represent an event in json format according to the following:

You will only be processing events from the `SITE_EVENT` topic. For each of these events you will produce a new `SITE_ANALYTICS` event with the following json structure:

```json
{
    "topic": "SITE_ANALYTICS",
    "timestamp": "",
    "siteId": "",
    "create_type": "",
    "publish_type": "",
    "unpublish_type": "",
    "update_type": "",
    "visit_type": "",
    "clientIpAddressHash": "",
    "country":"",
    "latencyMs": ,
    "siteName": ""
}
```
#### Where
**topic:** Will alway be "SITE_ANALYTICS". <br>
**timestamp:** Timestamp from the source event. <br>
**siteId:** SiteId from the source event. <br>
**create_type, publish_type, unpublish_type, update_type, visit_type:** One-hot encoding of the source event's `type` field depending on it's value (see example below). <br>
**clientIpAddressHash**: Since IP Address is considered personal identifiable information (PII) it must be obfuscated. You can choose to hash, encrypt or mask (or any other transformation you deem best) the IP Address in the source event as long as one IP produces the same obfuscated value every time, and no two IPs produce the same obfuscated value. <br>
**country:** Country of origin of the IP Address in the source event.  You can use the API defined in `./api.spec.yaml` to retrieve the country for a given IP Address. The API requires a key to be passed in the `x-api-key` header. You may use  the following key: `OYNGzWVSux7XcP3Y7dqfY8khCEsCknQ06wgAaWAK` <br>
**latencyMs:** Latency in milliseconds from the source event. <br>
**siteName:** Site name from the source event. <br>


Example:

For the following input:
```json
{
    "topic": "SITE_EVENT",
    "timestamp": "2021-02-27T16:55:43.399Z",
    "siteId": "5648bb64-350b-4bfa-bfde-adc589227ae4",
    "action": {
        "type": "VISIT",
        "clientIpAddress": "111.70.215.156",
        "latencyMs": 10708445597881656
    }
}
{
    "topic": "USER_EVENT",
    "timestamp": "2021-02-20T04:00:51.200Z",
    "userId": "4ad0d6e5-f32b-45e6-8520-8a38196a2005",
    "action": {
        "type": "CREATE",
        "email": "Gerald.Kunze42@gmail.com",
        "plan": "BASIC"
    }
}

```

The expected output would be:
```json
{
    "topic": "SITE_ANALYTICS",
    "timestamp": "2021-02-27T16:55:43.399Z",
    "siteId": "5648bb64-350b-4bfa-bfde-adc589227ae4",
    "create_type": 0,
    "publish_type": 0,
    "unpublish_type": 0,
    "update_type": 0,
    "visit_type": 1,
    "clientIpAddressHash": "4fc70fc8305870f8dcd661fb43fbcc88db2075b1",
    "country": "TW",
    "latencyMs": 10708445597881656,
    "siteName": ""
}
```
**NOTES:**

- In this example the output only contains one event because you should only process the SITE_EVENT topic.
- `visit_type` is set to 1 and all other `*_type` fields to 0 because the source event was of type `VISIT`. For more information on One-Hot enconding: https://en.wikipedia.org/wiki/One-hot
-  The hash in `ClientIPAddressHash` is the result of hashing the `ClientIpAddress` with a SHA-1 algorithm, but you can choose what you think is best.
- `country` is set to `TW` based on the returned value from calling the API
- `SiteName` is empty because it wasn't present in the source event.  


# Tips on rocking this code challenge

## Writing clean, scalable and well-tested code

It’s important that you write clean, easy to understand, and testable code.

It's also important to use software engineering best practices like unit tests, especially since data is not always clean and predictable.

Before submitting your solution you should summarize your approach, build and run instructions (if any) in your `README`. Don't use this `README`, instead write your own and place it in the src folder. 

In addition to the source code, the top-most directory of your repo must include the `input` and `output` directories

If your solution requires additional libraries, environments, or dependencies, you must specify these in your `README` documentation. 

