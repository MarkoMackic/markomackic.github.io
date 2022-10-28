---
layout: post
title: Decentralized social network - PT2
author: Marko Mackic
categories: research
---

Well let's go further.. we ended the last part with showing git-hooks in action,
but we need to analyze the hook data, so we can see how we can use it.

### Git hooks data ( actually we'll explore git a bit )

In the last part we didn't include stdin recv,  and we also didn't filter `GIT_` 
env variables to have only the data we need. 

Let's change our `pre_receive.py` too :

```
import os
import sys

print(sys.argv, file=sys.stderr)

for line in sys.stdin:
    print(line)

git_params={k:v for k,v in os.environ.items() if k.startswith("GIT_")}

print(git_params, file=sys.stderr)

exit(1)
```


And now when we retry to push the from our `test` repo, we can see the following
(something alike, the `incoming dir` changes ..):

```
markomackic@m3o:~/Desktop/Workspace/peers/test$ git push --set-upstream a master:test
Enumerating objects: 2, done.
Counting objects: 100% (2/2), done.
Writing objects: 100% (2/2), 165 bytes | 165.00 KiB/s, done.
Total 2 (delta 0), reused 0 (delta 0)
remote: ['hooks/../../pre_receive.py', '']
remote: 0000000000000000000000000000000000000000 107d4a937317e10a875c40cfcba1c06f989a53d1 refs/heads/test
remote: 
remote: {'GIT_DIR': '.', 'GIT_QUARANTINE_PATH': '/home/markomackic/Desktop/Workspace/peers/a/.git/./objects/incoming-hNRUxi', 'GIT_OBJECT_DIRECTORY': '/home/markomackic/Desktop/Workspace/peers/a/.git/./objects/incoming-hNRUxi', 'GIT_EXEC_PATH': '/usr/lib/git-core', 'GIT_ASKPASS': '/snap/code/111/usr/share/code/resources/app/extensions/git/dist/askpass.sh', 'GIT_PUSH_OPTION_COUNT': '0', 'GIT_ALTERNATE_OBJECT_DIRECTORIES': '/home/markomackic/Desktop/Workspace/peers/a/.git/./objects'}
```


Now the question is how can we use this quarantine object, but for that,
our script must hold a bit before answering to client,
because git cleans it up when we're done with the hook execution. 

Sort of patch to previous `pre_receive.py`:
```
import sys
+import time
...
print(git_params, file=sys.stderr)
+time.sleep(3600)   
```

Now let's look up the the incoming-* folder

```
markomackic@m3o:~/Desktop/Workspace/peers/a/.git/objects/incoming-C89yWt$ find . -type f
./4b/825dc642cb6eb9a060e54bf8d69288fbee4904
./8a/946d6db3b2516394b5c5bb070c65d205aa22f0
```

And since files are zlib comporessed, let's show their real content 
( you remember our empty commit in test from previous chapter ):

```
markomackic@m3o:~/Desktop/Workspace/peers/a/.git/objects/incoming-C89yWt$ cat ./4b/825dc642cb6eb9a060e54bf8d69288fbee4904 | zlib-flate -uncompress
tree 0
markomackic@m3o:~/Desktop/Workspace/peers/a/.git/objects/incoming-C89yWt$ cat ./8a/946d6db3b2516394b5c5bb070c65d205aa22f0 | zlib-flate -uncompress
commit 189tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904
author Marko Mackic <markomackic@gmail.com> 1666994576 +0200
committer Marko Mackic <markomackic@gmail.com> 1666994576 +0200

yo! just testing
```

Well, that's not so interresting, let's actually make some files, commit them,
and then push:

```
cd ~/Desktop/Workspace/peers/test
echo "Some content in file a" > a.txt
mkdir directory
echo "Some content in file b" > directory/b.txt
echo "Some content in file a" > directory/a.txt # i'm the only one interesting !

git status # check everything is unstaged 
git add a.txt
git commit -m "Commiting file a"
git add directory
git commit -m "Our first directory"

git push --set-upstream a master:test
```

We get :

```
markomackic@m3o:~/Desktop/Workspace/peers/test$ git push --set-upstream a master:test
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 8 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (9/9), 747 bytes | 747.00 KiB/s, done.
Total 9 (delta 0), reused 0 (delta 0)
remote: ['hooks/../../pre_receive.py', '']
remote: 0000000000000000000000000000000000000000 185d6e3a34831dc53381379394dea107bfa2413c refs/heads/test
remote: 
remote: {'GIT_DIR': '.', 'GIT_QUARANTINE_PATH': '/home/markomackic/Desktop/Workspace/peers/a/.git/./objects/incoming-yaEVS5', 'GIT_OBJECT_DIRECTORY': '/home/markomackic/Desktop/Workspace/peers/a/.git/./objects/incoming-yaEVS5', 'GIT_EXEC_PATH': '/usr/lib/git-core', 'GIT_ASKPASS': '/snap/code/111/usr/share/code/resources/app/extensions/git/dist/askpass.sh', 'GIT_PUSH_OPTION_COUNT': '0', 'GIT_ALTERNATE_OBJECT_DIRECTORIES': '/home/markomackic/Desktop/Workspace/peers/a/.git/./objects'}
```


Ok, we notice we still have only a single ref update, that's cool.
Let's inspect the incoming directory:

```
markomackic@m3o:~/Desktop/Workspace/peers/a/.git/objects/incoming-yaEVS5$ find . -type f
./31/9e305ad93260e7e3f747f485138254bc53dea2
./ed/5c636ab8c98ec261b4c7c577ebe0d89b859944
./4b/825dc642cb6eb9a060e54bf8d69288fbee4904
./71/e1327bfeae91512b0a701ee8ff4fe977078739
./8a/946d6db3b2516394b5c5bb070c65d205aa22f0
./fc/7d32606418d3710aeffa6855c556a98978a58d
./93/d8b86dc469ad839cdfb9eb58197ecefd06d9ec
./74/9468a5b401c10f87ee5d2b2f2a8490096027c0
./18/5d6e3a34831dc53381379394dea107bfa2413c
```

Now we'll decompress individual files to see what are we dealing with:

```
markomackic@m3o:~/Desktop/Workspace/peers/a/.git/objects/incoming-yaEVS5$ find -type f -print0 | xargs -0 -I{} sh -c "printf '\n\n***********\n' && echo {} : && cat {} | zlib-flate -uncompress"
***********
./31/9e305ad93260e7e3f747f485138254bc53dea2 :
blob 23Some content in file b
***********
./ed/5c636ab8c98ec261b4c7c577ebe0d89b859944 :
commit 237tree fc7d32606418d3710aeffa6855c556a98978a58d
parent 8a946d6db3b2516394b5c5bb070c65d205aa22f0
author Marko Mackic <markomackic@gmail.com> 1666995357 +0200
committer Marko Mackic <markomackic@gmail.com> 1666995357 +0200

Commiting file a
***********
./4b/825dc642cb6eb9a060e54bf8d69288fbee4904 :
tree 0
***********
./71/e1327bfeae91512b0a701ee8ff4fe977078739 :
tree 69100644 a.txt�ظm�i���߹�X~����40000 directoryt�h�����]+/*��	`'�
***********
./8a/946d6db3b2516394b5c5bb070c65d205aa22f0 :
commit 189tree 4b825dc642cb6eb9a060e54bf8d69288fbee4904
author Marko Mackic <markomackic@gmail.com> 1666994576 +0200
committer Marko Mackic <markomackic@gmail.com> 1666994576 +0200

yo! just testing
***********
./fc/7d32606418d3710aeffa6855c556a98978a58d :
tree 33100644 a.txt�ظm�i���߹�X~����
***********
./93/d8b86dc469ad839cdfb9eb58197ecefd06d9ec :
blob 23Some content in file a
***********
./74/9468a5b401c10f87ee5d2b2f2a8490096027c0 :
tree 66100644 a.txt�ظm�i���߹�X~����100644 b.txt1�0Z�2`���G��T�Sޢ
***********
./18/5d6e3a34831dc53381379394dea107bfa2413c :
commit 240tree 71e1327bfeae91512b0a701ee8ff4fe977078739
parent ed5c636ab8c98ec261b4c7c577ebe0d89b859944
author Marko Mackic <markomackic@gmail.com> 1666995357 +0200
committer Marko Mackic <markomackic@gmail.com> 1666995357 +0200

Our first directory
```


Now these gibberish chars are because zlib decodes byte-to-byte,
but you can get the principle.
And you can also notice that though two files contain same text,
there is only a single blob with `Some content in file a`.

Anyways we got carried away a bit, but I don't see a problem with that as long
as we're exploring and learning something,
notice how this `incoming` directory looks so so similar to object database,
that's because it is, let's correct ourselves..

You know those environement variables we printed in the receive hook, well,
they are used when invoking the `git` so you could access the objects that are 
urrently in the quarantine, and also the objects in the main repository,
the two of them beeing: 

* `GIT_OBJECT_DIRECTORY` which points to the quarantine object database
* `GIT_ALTERNATE_OBJECT_DIRECTORIES` which points to the main repo object 
database (since it it plural, I suppose you could add more of these)

These two are combined so we can lookup git objects from any of these
( so we can compare across which is very important in our further work)

The others are used too, I assume `GIT_DIR` is used when invoking something like
`git status`, `GIT_EXEC_PATH` stores a path to git binary
( so I don't think git uses it, I think it's more for a hook program ),
`GIT_ASKPASS` probably when needing credentials to push/clone/fetch the remote,
`GIT_QUARANTINE_PATH` = `GIT_OBJECT_DIRECTORY` so not really sure if and why
that's used, also the `PUSH_OPTION` is used if client initiated the request with
push options. Yeah, I think we covered them all.

Now let's do a proper git objects listing:

```
markomackic@m3o:~/Desktop/Workspace/peers/a$ GIT_OBJECT_DIRECTORY=.git/objects/incoming-yaEVS5/ git cat-file --batch-check --batch-all-objects
185d6e3a34831dc53381379394dea107bfa2413c commit 240
319e305ad93260e7e3f747f485138254bc53dea2 blob 23
4b825dc642cb6eb9a060e54bf8d69288fbee4904 tree 0
71e1327bfeae91512b0a701ee8ff4fe977078739 tree 69
749468a5b401c10f87ee5d2b2f2a8490096027c0 tree 66
8a946d6db3b2516394b5c5bb070c65d205aa22f0 commit 189
93d8b86dc469ad839cdfb9eb58197ecefd06d9ec blob 23
ed5c636ab8c98ec261b4c7c577ebe0d89b859944 commit 237
fc7d32606418d3710aeffa6855c556a98978a58d tree 33
```

Nice !

Ok, so we introduced ourselves a bit with the pre-receive git hook, env vars,
the data we get from it.

### Conclusion and next steps

No conclusion so far, we're reseaching to see our options.

Next step would be to try to implement ADD_PEER functionality. And finally do some commit signing and verification. 

I think turning this to a PoC is taking me more time because I'm trying to
document the steps as I go through ( along with my research on all the
pieces that might be needed ), but anyways, hopefully it will be worth it
at the end, and if not, at least some lessons will be learned.

### Resources

* [https://jiby.tech/post/git-diff-empty-repo/](https://jiby.tech/post/git-diff-empty-repo/)
* [https://git-scm.com/book/en/v2/](https://git-scm.com/book/en/v2/)
* [https://git-scm.com/docs/githooks](https://git-scm.com/docs/githooks)
* [https://unix.stackexchange.com/questions/22834/how-to-uncompress-zlib-data-in-unix](https://unix.stackexchange.com/questions/22834/how-to-uncompress-zlib-data-in-unix)
* [https://matthew-brett.github.io/curious-git/reading_git_objects.html](https://matthew-brett.github.io/curious-git/reading_git_objects.html)
* [https://git.wiki.kernel.org/index.php/GitTips](https://git.wiki.kernel.org/index.php/GitTips)


### Chapters : 

* [Chapter 1]({% post_url 2022-10-26-decentralized-git-social-network %})
* [Chapter 2 - Me]({% post_url 2022-10-27-decentralized-git-social-network %})