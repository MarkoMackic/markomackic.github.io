---
layout: post
title: Decentralized social network
author: Marko Mackic
categories: brainstorming
---

A couple of days back, I had this idea, you know. I didn't try any of this btw. 

Before we dive in deeper, we need to define social network, it's a network of people 
who collaborate, share, and do basic 1-many and 1-one comm. No likes, no heart emojis,
no fucking bullshit, just the real deal ! Read notifications included :-)

### Preface 

Distribution is long time with us, since the beginning of the internet, idea was to connect PC-s 
into a network where everyone could connect to everyone else. 
People talk about this "brand new" Web3, you know, and it's not the concept that is new, it's 
just the industry standards that devietad from initial web concept, creating more centralized
environment, but I understand that, it's easier to manage, and most certianly it's easier to
implement. Anyways, distribution is really known to all of us, we all used `torrents`, some of
us seeded them, we use `git` now in our everyday work, basically the concept is data duplication
so a single unit may fail safely without danger that data will be lost.

### Social network with e2e encrption using `git`

Now, imagine the repository layout like this:

```
repository
|-peer_repos
| |-somewhere_hosted_repo.json (let's say this is our initial server, we must start somewhere)
| |-somwhere_else_hosted_repo.json (whatever else)
|-common_hook_impls
| |-git-hook-update
| |-git-hook-pre-recieve 
|-users
| |-markomackic_(main_hosting_repo e.g somewhere_hosted_repo)
| | |-uinfo.json -> contains user info like username, main_hosting_repo,  mail (optional, we like anonymous people with skill!!), and also contains gpg pubkey
| | |-msgs
| |   |-user2_(main_hosting_repo)
| |     |-message_1.txt -> contains message from user2 -> markomackic crypted with markomackic gpg pubkey
| |-user2_(main_hosting_repo)
|   |-uinfo.json
|   |-msgs
|     |-markomackic
|       |-message_1.txt -> markomackic -> user2 crypted with user2 gpg pubkey
|
|-posts
  |-markomackic_(main_hosting_repo)
    |-post1.md 
  |-user2_(main_hosting_repo)
    |-post1.md

```


#### Concept 1 - NO_DELETE, NO_EDIT, SINGLE_FILE_COMMIT

It's really simple, files can just be added, which means unique fnames, which means no conflicts.
And a single commit contains only a single file, post to everyone, or message to someone!



#### Concept 2 - SIMPLE_COMMIT_MSG

Now let's introduce the commit messages, we'll have a couple of them ( very restricted range ): 

```
PEER_VIOLATION/{WHOAREYOU}
USER_VIOLATION/{WHOAREYOU_PEERNAME}
ADD_USER/{WHOAMI}_{PEERNAME}
ADD_PEER/{WHOAMI}
SEND_MESSAGE/{FROM}/{TO}
POST_SOME_SHIT/{FROM}
```

Simple as that ! This will help us with the verifications. It's not strict, might change.

#### Concept 3 - PUSH_POLICY

Simple push policy, no force-push allowed !

#### Concept 4 - VERIFICATION and the beaty of git hooks.

Now we'll need to go a bit deeper. We'll need to write some code, as well as explain everything in the process.
We will just make a proof of concept, we won't implement everything.

I'm using linux, so if you have one, you can follow along this journy.. 

First some basic info 

```
markomackic@m3o:~/Desktop/Workspace/peers/a$ python3 -V
Python 3.8.10
markomackic@m3o:~/Desktop/Workspace/gtest$ git --version
git version 2.25.1
markomackic@m3o:~/Desktop/Workspace/gtest$ gpg --version
gpg (GnuPG) 2.2.19
libgcrypt 1.8.5
Copyright (C) 2019 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Home: /home/markomackic/.gnupg
Supported algorithms:
Pubkey: RSA, ELG, DSA, ECDH, ECDSA, EDDSA
Cipher: IDEA, 3DES, CAST5, BLOWFISH, AES, AES192, AES256, TWOFISH,
        CAMELLIA128, CAMELLIA192, CAMELLIA256
Hash: SHA1, RIPEMD160, SHA256, SHA384, SHA512, SHA224
Compression: Uncompressed, ZIP, ZLIB, BZIP2
markomackic@m3o:~/Desktop/Workspace/gtest$ 
```

We need a workspace first  

```
cd ~/Desktop/Workspace
mkdir gpg
cd gpg 
mkdir a
mkdir b
mkdir c
```

So let's generate a couple of gpg keys .. 

```
> GNUPGHOME=~/Desktop/Workspace/gpg/a gpg --generate-key
Real name: a_server
Email: a_server@a_server
Passphrase: a_server

> GNUPGHOME=~/Desktop/Workspace/gpg/b gpg --generate-key
Real name: b_server
Email: b_server@b_server
Passphrase: b_server

> GNUPGHOME=~/Desktop/Workspace/gpg/c gpg --generate-key
Real name: c_server
Email: c_server@c_server
Passphrase: c_server
```

We needed to separate the keyrings of each one, since ADD_PEER wouldn't be properly tested if they were in the default one.. 

Ok, now it's time to initialize the create the peers .. simple git repos !

```
cd ~/Desktop/Workspace
mkdir peers
cd peers
git init a 
git init b
git init c

# this won't be peer repo, this will be used to test the hooks while developing 
git init test
```

So we `cd a` and `ls -a`, we can see the `.git` directory. The focus of our experiment is `hooks` inside.
There are some samples but we're going to use Python for hooks development, because I don't really wanna
test my Bash skills.

So inside dir `a`:

```
cd .git/hooks
echo -e "#! /usr/bin/env bash\npython3 -u \`dirname \$0\`/../../pre_receive.py \"$@\"" > pre-receive
```

Here is the content of `pre-receive` for more readability (we don't actually need the comments, so yeah): 
```
#! /usr/bin/env bash
#
# The "pre-receive" hook is the first hook to be executed when handling
# a push from a client. It takes a list of references being updated
# from stdin. A non-zero status code causes the entire push request
# to be rejected, meaning that none of the references get updated.

python3 -u `dirname $0`/../../pre_receive.py "$@"
```

And now let's write `pre_receive.py` inside `a`:

```
import os
import sys

print(sys.argv, file=sys.stderr)
print(os.environ, file=sys.stderr)

exit(1)
```

for a start ..

Let's test the hook ..  You remember that `test` repo we inited.

We'll execute 

```
cd test 
git remote add a ../a # add a remote
git remote -vv # check that a is in the remotes
git commit -m "yo! juste testing" --allow-empty # commit something dumb
git push --set-upstream a master:test # try to push our master to test branch of a, and see denial with a much of giberrish!!!
```


#### Todays session conclusion 

We'll have other parts of this that will be in more detail ( directory structure and commit messages may deffer, we're in the process)
But I hope I gave you some insigths into my plan to conceptually make this. 
When second part is written, I'll update this post with a link.. 

Good night, ya all!


#### Resources 

* [https://unix.stackexchange.com/questions/481939/how-to-export-a-gpg-private-key-and-public-key-to-a-file](https://unix.stackexchange.com/questions/481939/how-to-export-a-gpg-private-key-and-public-key-to-a-file)
* [https://stackoverflow.com/questions/54461319/gpg2-how-to-use-another-secret-and-public-keyring](https://stackoverflow.com/questions/54461319/gpg2-how-to-use-another-secret-and-public-keyring)
* [https://github.com/AdaCore/git-hooks](https://github.com/AdaCore/git-hooks)
  * Nothing special learned/used from here, but the research led me to this url, so there it is.  
