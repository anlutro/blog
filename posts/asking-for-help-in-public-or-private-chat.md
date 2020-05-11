# Asking for help in public or private chat
pubdate: 2020-05-10 19:42 CEST
tags: Communication, Company culture

Here's a pattern I've seen in multiple organizations: If someone is stuck with a problem, they guess who might know the solution to that problem and ask them privately, either in person or over chat (e.g. Slack). I always preferred to be asked over chat rather than in-person because it means I can postpone reading it for 5 minutes if I'm in the middle of something, and now with remote working being pretty much mandatory, the in-person option isn't even there any more.

I think this is a bad habit, and something that should be discouraged especially in engineering departments. First, let's outline the advantages of asking in private, usually the reasons why people default to doing it:

- You don't feel like you're bothering everyone in the channel who might not care about your problem. 
- You're guaranteed to get someone's attention, your question is very unlikely to be ignored.
- It *feels* similar to what you would do in real life: Walk up to a colleague and ask them if they have time to help.

While these points are technically correct, I also think they're based on flawed premises, which we will get back to. For now, let's list the drawbacks of asking for help in private:

- You have to know who to ask.
- If you ask the wrong person, you've potentially interrupted them without really achieving anything.
- If you ask the wrong person and you are referred to someone else, or you just guess someone else who might know, you're asking your question N times which wastes your time. This gets especially annoying if your question isn't a simple copy-and-paste one, for example if there are follow-up Q&A or additional context added after the fact.
- If the person you ask gives you an answer, that answer may be incorrect or inefficient, and another colleague might be able to correct them - but because your messages are private, they can't.
- Other colleagues cannot read your question and answers given to your question, and hence cannot learn from it.
- It gives the impression that no one is asking for help, which can discourage others (especially new joiners) from asking for help.

It's worth noting that this is slightly different when **not** working remotely - if I walk over to a colleague in the office and ask them for help and we discuss the problem in person, others can overhear our discussion if they're not too busy with other things, and we avoid a lot of the problems mentioned above.

So what should you do instead? Ask in a public chat channel. Even [Slack itself claims it's the ideal](https://slackhq.com/slack-103-communication-and-culture):

> Slack is designed to add transparency to an organization, so it’s best to default to communication in public channels whenever possible. Slack’s own team sends tens of thousands of messages each week—in a recent summary, 70% of those were posted in public channels, with 28% occurring in private channels and just 2% in direct messages. Posting messages in public channels means anyone in the organization can see what various teams are working on, see how much progress people are making on projects, and search the archive for context they need.

Here are some tips for successfully asking for help in public chat channels:

- If you're not sure which channel is the best fit, just put it in the most generic one. Most engineering companies have channels like `#dev-example-app` or just `#development`.
- If your question is long and you don't want to flood the channel with text, summarize your question in a short paragraph then elaborate on it in a thread. This has the added bonus of encouraging others to use threads as well.
- If you're worried that putting your question in a public chat channel will create noise for others, actually verify if this is the case. Are you bothered any time a question is asked in a public channel? Ask some colleagues in one-on-one situations what they think as well. In my experience, no one enables sound or pop-up notifications for channel messages. But if this is actually a problem somehow, consider creating dedicated channel(s) (e.g. `#dev-help`) for asking for help that can more easily be muted.
- If, after some time (let's say an hour), you haven't resolved your question, consider mentioning colleagues who you suspect might be able to help (the people you would consider asking for help in private). You can do this either by sending a link to your question in a private message, or mentioning them in the channel/thread itself.
- If you haven't resolved your question after a long amount of time (let's say 24 hours), simply post the question again and specify that you didn't get an answer within 24 hours.
- If the question remains unresolved for even longer, you'll either have to escalate to your manager, or accept that no one actually knows and you'll have to figure out for yourself.
