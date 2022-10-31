---
layout: post
title: Decentralized social network - PT3
author: Marko Mackic
categories: research
---

Now let's discuss a bit about about gpg and hopefully
implement the ADD_PEER today. 

### GPG

You remember the keys we generated in the first part. Well we'll finally 
use them in this part.

There are two things we're interested in, asymmetric encription, and signing.

So let's try some of these things 

```
cd ~/Desktop/Workspace/gpg
mkdir test
cd test
```

Ok now, let's list keys 

```
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=~/Desktop/Workspace/gpg/a gpg --list-keys
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/a'
/home/markomackic/Desktop/Workspace/gpg/a/pubring.kbx
-----------------------------------------------------
pub   rsa3072 2022-10-27 [SC] [expires: 2024-10-26]
      7CD8D3B71C0FFDEF735A222255D3D067984819DC
uid           [ultimate] a_server <a_server@a_server>
sub   rsa3072 2022-10-27 [E] [expires: 2024-10-26]
```

Cool, we have only `a_server`, let's export it's public key.
We're interested in exporting only single key ( though in this case we have only one),
but anyways, we'd like to have `uid` specifed when exporting the key. So first let's
prove we error on specifying wrong user ( the query isn't fully validated, I think 
it uses just `uid`.`startsWith`), because if we'd use `a` instead of `a_servar` it 
would export the key ..  

```
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=~/Desktop/Workspace/gpg/a gpg -a --export a_servar
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/a'
gpg: WARNING: nothing exported
```

Ok, now we'll export the key into a file `a_pubkey.asc`  

```
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=~/Desktop/Workspace/gpg/a gpg -a --export a_server 2>/dev/null > a_pubkey.asc
markomackic@m3o:~/Desktop/Workspace/gpg/test$ ls
a_pubkey.asc
markomackic@m3o:~/Desktop/Workspace/gpg/test$ cat a_pubkey.asc 
-----BEGIN PGP PUBLIC KEY BLOCK-----

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
WHx0loY3gFawe+gCEwvAiS6+2Io=
=+WOf
-----END PGP PUBLIC KEY BLOCK-----
```

Export the `b` and `c`:

```
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=~/Desktop/Workspace/gpg/c gpg -a --export c_server 2>/dev/null > c_pubkey.asc
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=~/Desktop/Workspace/gpg/b gpg -a --export b_server 2>/dev/null > b_pubkey.asc
```

Now let's go further, let's create another gpg home directory and include the pubkeys of servers.

```
mkdir server_keys

markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=./server_keys/ gpg --import a_pubkey.asc 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/./server_keys'
gpg: key 55D3D067984819DC: public key "a_server <a_server@a_server>" imported
gpg: Total number processed: 1
gpg:               imported: 1
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=./server_keys/ gpg --import b_pubkey.asc 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/./server_keys'
gpg: key F7391DAF9F8B70F5: public key "b_server <b_server@b_server>" imported
gpg: Total number processed: 1
gpg:               imported: 1
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=./server_keys/ gpg --import c_pubkey.asc 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/./server_keys'
gpg: key 67513C9812C14D6B: public key "c_server <c_server@c_server>" imported
gpg: Total number processed: 1
gpg:               imported: 1

markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=./server_keys/ gpg --list-keys
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/./server_keys'
/home/markomackic/Desktop/Workspace/gpg/test/./server_keys/pubring.kbx
----------------------------------------------------------------------
pub   rsa3072 2022-10-27 [SC] [expires: 2024-10-26]
      7CD8D3B71C0FFDEF735A222255D3D067984819DC
uid           [ unknown] a_server <a_server@a_server>
sub   rsa3072 2022-10-27 [E] [expires: 2024-10-26]

pub   rsa3072 2022-10-27 [SC] [expires: 2024-10-26]
      FBE8597BC4C58FAC01E08FE4F7391DAF9F8B70F5
uid           [ unknown] b_server <b_server@b_server>
sub   rsa3072 2022-10-27 [E] [expires: 2024-10-26]

pub   rsa3072 2022-10-27 [SC] [expires: 2024-10-26]
      FD052B680E57ABF5D178FB2467513C9812C14D6B
uid           [ unknown] c_server <c_server@c_server>
sub   rsa3072 2022-10-27 [E] [expires: 2024-10-26]
```

Nice, we have the keys db with all server pubkeys .. Let's 
create a simple document, and check the signing and encryption. 

Ok, signing first. 

```
mkdir keys_armored 
mv *.asc keys_armored # just so we have some structure

echo "This is a content signed by A" > a_singed.txt
echo "This is a content signed by B" > b_singed.txt
echo "This is a content signed by C" > c_singed.txt

markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=../a gpg --batch --pinentry-mode loopback --passphrase a_server --sign a_singed.txt
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=../b gpg --batch --pinentry-mode loopback --passphrase b_server --sign b_singed.txt
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=../c gpg --batch --pinentry-mode loopback --passphrase c_server --sign c_singed.txt

markomackic@m3o:~/Desktop/Workspace/gpg/test$ ls
a_singed.txt  a_singed.txt.gpg  b_singed.txt  b_singed.txt.gpg  c_singed.txt  c_singed.txt.gpg  keys_armored  server_keys

markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=./server_keys gpg --verify a_singed.txt.gpg 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/./server_keys'
gpg: Signature made nedjelja, 30. listopada 2022. 22:16:17 CET
gpg:                using RSA key 7CD8D3B71C0FFDEF735A222255D3D067984819DC
gpg: Good signature from "a_server <a_server@a_server>" [unknown]
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 7CD8 D3B7 1C0F FDEF 735A  2222 55D3 D067 9848 19DC
```

Ok, nice, we see we have a valid signature but it's not trusted. To trust the 
key we'd need to sign it with our private key, so let's do it, first generate
the keys.. 

```
GNUPGHOME=./server_keys gpg --generate-key
Real name: test_server
Email : test_server@test_server
Passphrase: test_server
```

```
GNUPGHOME=./server_keys gpg --yes --batch --pinentry-mode loopback --passphrase test_server --sign-key a_server # now we trust the a_server

markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=./server_keys gpg --verify a_singed.txt.gpg 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/./server_keys'
gpg: Signature made nedjelja, 30. listopada 2022. 22:16:17 CET
gpg:                using RSA key 7CD8D3B71C0FFDEF735A222255D3D067984819DC
gpg: checking the trustdb
gpg: marginals needed: 3  completes needed: 1  trust model: pgp
gpg: depth: 0  valid:   1  signed:   1  trust: 0-, 0q, 0n, 0m, 0f, 1u
gpg: depth: 1  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 1f, 0u
gpg: next trustdb check due at 2024-10-26
gpg: Good signature from "a_server <a_server@a_server>" [full]

markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=./server_keys gpg --verify b_singed.txt.gpg 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/./server_keys'
gpg: Signature made nedjelja, 30. listopada 2022. 22:17:29 CET
gpg:                using RSA key FBE8597BC4C58FAC01E08FE4F7391DAF9F8B70F5
gpg: Good signature from "b_server <b_server@b_server>" [unknown]
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: FBE8 597B C4C5 8FAC 01E0  8FE4 F739 1DAF 9F8B 70F5
```

Cool :) Let's also prove everyone can read the data ( since we only signed, we didn't encrypt)

```
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=./server_keys/ gpg --decrypt a_singed.txt.gpg 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/./server_keys'
This is a content signed by A pubkey
gpg: Signature made nedjelja, 30. listopada 2022. 22:16:17 CET
gpg:                using RSA key 7CD8D3B71C0FFDEF735A222255D3D067984819DC
gpg: Good signature from "a_server <a_server@a_server>" [full]

markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=../a gpg -a --decrypt a_singed.txt.gpg 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/../a'
This is a content signed by A pubkey
gpg: Signature made nedjelja, 30. listopada 2022. 22:16:17 CET
gpg:                using RSA key 7CD8D3B71C0FFDEF735A222255D3D067984819DC
gpg: Good signature from "a_server <a_server@a_server>" [ultimate]

markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=../b gpg -a --decrypt a_singed.txt.gpg 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/../b'
This is a content signed by A pubkey
gpg: Signature made nedjelja, 30. listopada 2022. 22:16:17 CET
gpg:                using RSA key 7CD8D3B71C0FFDEF735A222255D3D067984819DC
gpg: Can't check signature: No public key

markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=../c gpg -a --decrypt a_singed.txt.gpg 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/../c'
This is a content signed by A pubkey
gpg: Signature made nedjelja, 30. listopada 2022. 22:16:17 CET
gpg:                using RSA key 7CD8D3B71C0FFDEF735A222255D3D067984819DC
gpg: Can't check signature: No public key
```

Yeah, everyone can get the content :) Also to mention it's better to use `clearsign` 
when working with the text content, but for now it doesn't matter.. 

Nice, let's go further.

Now we're going to test e2e encryption ..

Let's first remove the files we had, we don't care about them anymore.

```
rm *.txt *.gpg
```

OK, let's continue, we're going to send from `test` to `a` because 
we have `a` pubkey in `test` keyring already.

```
echo "This is a message from test to A" > test_a_message.txt
GNUPGHOME=./server_keys/ gpg -u test_server -r a_server -e test_a_message.txt 

# Not even we can decrypt it 
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=./server_keys/ gpg -d test_a_message.txt.gpg 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/./server_keys'
gpg: encrypted with 3072-bit RSA key, ID 8F71224F64E2B23C, created 2022-10-27
      "a_server <a_server@a_server>"
gpg: decryption failed: No secret key

# Well that's nice
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=../a gpg --batch --pinentry-mode loopback --passphrase a_server -d test_a_message.txt.gpg 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/../a'
gpg: encrypted with 3072-bit RSA key, ID 8F71224F64E2B23C, created 2022-10-27
      "a_server <a_server@a_server>"
This is a message from test to A

# Try with b
markomackic@m3o:~/Desktop/Workspace/gpg/test$ GNUPGHOME=../b gpg --batch --pinentry-mode loopback --passphrase b_server -d test_a_message.txt.gpg 
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/gpg/test/../b'
gpg: encrypted with RSA key, ID 8F71224F64E2B23C
gpg: decryption failed: No secret key

# Super cool ..
```

Well e2e works, now let's talk about `ADD_PEER` 

## ADD_PEER

You remember our first part, and that directory layout, well for this part
we're going to focus on this part ( we substitued ) :

```
repository
|-peer_repos
```

ADD_PEER is a single commit which consists of a file named `{SERVER_NAME}.json`,
in our current context those would be `a_server.json`, `b_server.json`, `c_server.json`.
Let's define the format ( we'll use `a` as example ), pubkey is `base64` encoded:
```json
{
    "server_name": "a_server",
    "server_mail": "a_server@a_server",
    "server_repo": "network reachable git endpoint, but in our example we'll use file://",
    "pubkey": "LS0tLS1CRUdJTiBQR1AgUFVCTElDIEtFWSBCTE9DSy0tLS0tCgptUUdOQkdOYThXb0JEQURNd1p4U241OEd2d3VMV0hvQ2o5aUkvdFlCTjcyRFVYSTZld0kvV2RaUXlsRktSME1ICnIvUno1YS8wK1lKZHQrMTZDc0NiY2dMbUJMSE5NcjA4L2dSVzFQNkZ3bTVEWEFsaGg5NUltQUpNZlZ3M01iM2kKZ3Y5U3Q1OXl1WUVvd0lRREZkU3F5TGxhWkJKNW11TkRpcUJXS05ibjdPbXlTS1BlUDVYU0FKMmFrZGxTc1VELwpOUHBHYU9xVU03dUhCMmZPTU5vMzVuUkF1d1cwMUZlZVYxcDRsMkFTUUo3elVGdWkwTFZUYU16UjNRUkRPTHE0CjlKTVlKSUhyckFFOVNpZGJWalhNcXgyUk5BQ2NpU2lXTzNaTkpxbkFDVlFseGs1M0FCZmVWNSsxV2poc0VTamcKRzMzNlo1eU4wdnV1ZEtZUUdCK2h2Nk5xd3M0OTBJSk1kSFFIbkFrSGVYWFIvTzN6YVBTcGVHYVFkS2hTYWEwOQpDaDY3eWQ2RU9DNHBiSlZuRzIzeTJoSzRVQTN6WHA2Q1ZyNnZ2NURCL0d4ZUJsK2xNZ1FVNlVLMkN1b0licDgrCk9vNng0WjJ2aFA5bUpuZGdtNzZQa2NGSmRwMHVhdXAwQ1lqSXI1WlBvM1duRlhGOGdPZzh5NXVSUmVpOXB2ZlEKdFJrNVlkWExobWllb2hzQUVRRUFBYlFjWVY5elpYSjJaWElnUEdGZmMyVnlkbVZ5UUdGZmMyVnlkbVZ5UG9rQgoxQVFUQVFvQVBoWWhCSHpZMDdjY0QvM3ZjMW9pSWxYVDBHZVlTQm5jQlFKald2RnFBaHNEQlFrRHdtY0FCUXNKCkNBY0NCaFVLQ1FnTEFnUVdBZ01CQWg0QkFoZUFBQW9KRUZYVDBHZVlTQm5jc2dZTUFLMjYrZmxuaDFSVVphbmsKSWFGRHlsN2R6eDE5RUVkS3JXY1NYSlJaanV1Qk00cHZaU0g1RzJvYUJBcnhqbTk1ZHVkTXdDRERmYzd3M29nQQpQZnI4amFCL3FQU3FCbkg3RFAwUUc5VUJwMkQrcDQ2R0ZGSE1pT2tJM2FKNjJTelZPMTRCaXZuRmg5clZQclEvCkIraW80Vk9MN3B6Q0I2d2ltMkN0RnZVWnJ1TERGUEFib3VtaisyUTRXWDlFK3pxd2VZTkJ6ZjI0bFBlZytBRUUKTHhZWmtuNUhEVFJoV3VPRjkvNDJhRmFrRE9TRythaUNwSEV5amJxZStQWXpsL2pCWkRPK3ZrTWZCbUVQeGtPWAp3VHYrMTFBUTAvUlFJTlo4Nm9KbUViMGY4aU13M2dsbVAzKzA3KzE3N3VoWjNwNkVzRFpFSCtCLzl2UzdydmNDCk1meEc1T3V0MmZNbmxUeVVNWVp3OTRnVW92ZmE2dnFhQ3JDME1IWjZEU1BMdkJEbndjRFNEVld6azk4TXMzc2UKaUdja3FjQ0dJN1NwTTJzMzlXVFVEZjNPVU0wNkVjVVY2amVteThud2ExVHlzVUNTa04zVlkzRC9zL2R5Rk5KLwprYmFiVVdITk9MdnpBVy9TbFhWVExoUUZEZUpTNkhxbWtTU0twWGJPeHUrdExtQWhTYmtCalFSald2RnFBUXdBCjBUK1lITVp3NGY0Q0duNCtiMS9lcUxsY3RoekVaZTdJMElkQ3gwaTNTL3lqQnFCNkplSENmVVNVM2xHdFBKMzMKbFNCV0p5L29oYTNHUTlNRUgyQlZiSDNxcXJHd0pNSEdZNG5tVFJUekVpNHMzZldGQUgyK3hBWFVLRXJ2TXVUTwpzdmMvSmpuRmRZWmRyRWZRdHoxU2RJbGlJa2JvS3hWQkl4cG0rcjZ0NmNiWG04c3Q0bHIrV0c5cTMzc0xwckR5CnlOUHBpRm15VWxUaUZuaVgxV0JSVFVYWjJlZ2hndjBsaW5sSEVKcWlXT001aVRPNnB3eVJTUjhlczhTQStMajkKajF1cHNZLzhwTGxkZmdpUCs3SGlYeGRQZ2NyZGltSnlHc2FXVkRES1N0cEpmZ3RTVG80RmFaZHlPVEFHdVlRVwpOZkZ6S1NWU0N2UXNBbWZYQTIrdmNIS1A2ZTJUVEh1NnhKaXZOUU9UNnJyU0RVdDBhdzBvd0REMEtCYkkxU1VRCkR2TXpTVEFaZmEwRXpwRHJaaXgvMjZxemNaVmhjcmRPdzNoSXpKVnZzZ2wzNVBNUFc5ZzRRSENWZFFIblRabkgKQ1RGdnphVElYejRLR3piOC9ERGZCM2FoekY1TnBKdlVLMUlzNVlaVnZJWjRpd3lEUm1pbENFdWRaR0FWS0Z1NwpBQkVCQUFHSkFid0VHQUVLQUNZV0lRUjgyTk8zSEEvOTczTmFJaUpWMDlCbm1FZ1ozQVVDWTFyeGFnSWJEQVVKCkE4Sm5BQUFLQ1JCVjA5Qm5tRWdaM0dScEMvNG9XcHdIUGxnNGlLT2ZvYkN5M2V0eFF5eFE5R09FZTRTazBTdVIKYVVvRUdKdmtnR1JobHNFb0FCUktKS2NXNytjOG5yRndxSFRNbStub0p2bXd2RXF4alJKeFhxRmY0NDlNYkxEOAo4NTIzZlRKVmxabGRmTVFGM0hiTzZPYmVxRVkzSDZmdTN3c2d3TzUyWDZ5bmlDdXE3QkF6aGowWk9XbXc1RnM1ClNjVHdTNTUzRy9WVTJVTktHUDJlUkl5VG0yTTE4TDVzS05NYUxQbkNGZzI2MW16TmhPbFhMYy9yS2FJNGJiTWcKd1RJaHdaWXVnY0I1NGFFSjA3QjlTOWF6emFzQkoxcjIvVlVKUnNZVEpucFZMdVRVM3RYb1NFYWo3cDR1ZkIyTgorV1VYemd2Z2k4NHJWd1NZRmd5Tk9vK3krZjBEOXRLS0FCNkFQa1N3SVYyUEhSYWF2Q3k2ZytkR1ZMUnZWdjVnClJXaWpVcmtEaUorZFptZHduVy92eUlCVlp1ZWtDTmRqdFJTb2NKZGZpZU1KRFNtVjlFNFRIQ2FWWmhIREttcUMKM0h3YXNOL0xyMGloSysrb2RpUk8xeTE1TnJwRWRIS3JHRVpFQXBSNGhEd092UTU1U3BEWEw5NVZvY2JLN1NSOQpXSHgwbG9ZM2dGYXdlK2dDRXd2QWlTNisySW89Cj0rV09mCi0tLS0tRU5EIFBHUCBQVUJMSUMgS0VZIEJMT0NLLS0tLS0K"
}
```

This commit must be signed from `a_server`. 
Because we're using repo `a` for testing hooks, let's create this in `b` and then see
how to verify it in `a`.

```
cd ~/Desktop/Workspace/peers/b
mkdir peer_repos
base64 -w 0 ../../gpg/test/keys_armored/b_pubkey.asc | xargs -I{} printf '{"server_name": "b_server", "server_mail": "b_server@b_server", "server_repo": "file:///home/markomackic/Desktop/Workspace/peers/b", "pubkey":"{}"}' > peer_repos/b_server.json
```

Cool, we have generated server description, now we'll have to do a bit of git moddification,
so it wouldn't ask us for credentials.. although we do have to do only single commit,
but it will be useful to get this right away, becauseOk, let's have this changed pre-receive hook in the a repository ( I did a bit of work 
in between without you watching every step, but nothing that you can't understand )
 signing. 

```bash
git config --local --add gpg.program /home/markomackic/Desktop/Workspace/peers/b/.git/bin/gpg.sh
```

```
mkdir .git/bin # already local only to us
echo -e '#/bin/bash\ngpg --batch --pinentry-mode loopback --passphrase $GPG_PASSPHRASE $@' > .git/bin/gpg.sh
chmod +x .git/bin/gpg.sh
```

`gpg.sh` :

```bash
#/bin/bash
gpg --batch --pinentry-mode loopback --passphrase $GPG_PASSPHRASE $@
```

Ok nice, let's try to add our work and sign the commit .. 

```
echo RELOADAGENT | gpg-connect-agent # well I'm not sure if this works, anyway, should purge gpg auth cache
git add .
GNUPGHOME=../../gpg/b/ GPG_PASSPHRASE=b_server git commit -Sb_server -m "ADD_PEER/b_server" # Sign the work 

markomackic@m3o:~/Desktop/Workspace/peers/b$ GNUPGHOME=../../gpg/b git log --show-signature
commit 857e920eb30a839e3ece9d8be65d71c57c1a3aed (HEAD -> master)
gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/peers/b/../../gpg/b'
gpg: Signature made ponedjeljak, 31. listopada 2022. 00:49:27 CET
gpg:                using RSA key FBE8597BC4C58FAC01E08FE4F7391DAF9F8B70F5
gpg:                issuer "b_server@b_server"
gpg: Good signature from "b_server <b_server@b_server>" [ultimate]
Author: Marko Mackic <markomackic@gmail.com>
Date:   Mon Oct 31 00:49:27 2022 +0100

    ADD_PEER/b_server
```

Just to say commit sha difference between logs is caused by me resetting the repo
to test things. 

```
git remote add a ../a 
git push --set-upstream a master:peers/b_server

We get that gibberish from our pre-receive hook, that's 
all nice.
```

Well, Houston, we have a problem! 

Yeah, the hook works and all, but we can't prove `b` is 
actually pushing to `peers/b_server` branch of `a`.. So before any
further work we need to address that. 

But `git` doesn't fail us here ( Thanks GIT ! )

What we'll do is sign the `SHA` of the last commit in detached 
mode (we have data avalible on both server and client so it doesn't
need to be included ), pipe it to `base64` and then send it with
`--push-option SIGNATURE:{sha_signed_content_base64}`. Nice !

Before we do that we should go to `a` and enable push options.

```
cd ../a
git config receive.advertisePushOptions true
cd ../b    
```

Now let's try to do that and compose it into readable command:

```
markomackic@m3o:~/Desktop/Workspace/peers/b$ cat .git/refs/heads/master | tr -d "\n" | GNUPGHOME=../../gpg/b gpg --batch --pinentry-mode loopback --passphrase b_server -o - --armor --detach-sign 2>/dev/null | base64 -w 0 
LS0tLS1CRUdJTiBQR1AgU0lHTkFUVVJFLS0tLS0KCmlRR3pCQUFCQ2dBZEZpRUUrK2haZThURmo2d0I0SS9rOXprZHI1K0xjUFVGQW1OZjYzSUFDZ2tROXprZHI1K0wKY1BWTkJBdi9VK1VoOUgyMFlZaXhFZmt2VERRcTRLRitvd1J5Wis1aXd0Z2haQnpGY05MdEVqR1NFeTRJWStMYgpsK0NBUXlPWlNzOVBTWk95Z25OYjhhNFlYaGFTbkRGMmNGTDVyVVhMbVpMZWgxOU5GSnB5MEFUVVpGcDV4Z2JkCkpIWVJCblB2UktYUW81eFhNVkRxWHJmM01OZnpwdWJ6L08wb0ErT05tMG9iQ2NwT0ZFZThEL3c1a2NpcWtpM1AKdW4rNTZBTTRLMERzNzFNYUtYcmdWbFJ1a0JOajZ0d2hSaHBKazBzQkQ1a1FLNWxHTFhWTXh0S29MM3Y4TkJlcApXRW0wa3k0WERXb3VWNmd3Z29MT1Vrb3FmWG1IRzM4NEthT0cvRUtpZi9wT1R0VFlLOGkyS28rUDQ5TEpxN3IxCkFEOVQxMzdLem5nbWJSTEZpVFpMRFQ0VWJWVGlYUWYxSnMrVlpydHBEYmUvZC94ZDZWYkZCVStDTTlpblBwNDIKWWNTYzFZRVl1TkJSUzcrc3QzZWYxUERIS2p3L1dMSUtaNHJwUFVqODY4Mkk4NmpHNEFiQmRTNlZTN0FvdXRLWQpQMVdVRGFCU1RNWXd1bHhjVHRaMlphT2kzYVArTUxOWTdrRFZJMDQ0Q2ZHNWJaNTUvVyt5VEs0dm04c29EUDVhCmdETGJyTFR1Cj04b2ZSCi0tLS0tRU5EIFBHUCBTSUdOQVRVUkUtLS0tLQo=

# YO, YO , nice :)

markomackic@m3o:~/Desktop/Workspace/peers/b$ git push --push-option SIGNATURE:$(cat .git/refs/heads/master | GNUPGHOME=../../gpg/b gpg --batch --pinentry-mode loopback --passphrase b_server -o - --armor --detach-sign 2>/dev/null | base64 -w 0) --set-upstream a master:peers/server_b
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 8 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (4/4), 3.21 KiB | 3.21 MiB/s, done.
Total 4 (delta 0), reused 0 (delta 0)
remote: ['hooks/../../pre_receive.py']
remote: export GIT_DIR=.
remote: export GIT_QUARANTINE_PATH=/home/markomackic/Desktop/Workspace/peers/a/.git/./objects/incoming-AK24Oc
remote: export GIT_PUSH_OPTION_0=SIGNATURE:LS0tLS1CRUdJTiBQR1AgU0lHTkFUVVJFLS0tLS0KCmlRR3pCQUFCQ2dBZEZpRUUrK2haZThURmo2d0I0SS9rOXprZHI1K0xjUFVGQW1OZjdKTUFDZ2tROXprZHI1K0wKY1BYRjF3d0FuSW5IaGFtUW5GclFKUnBvY3BKeDdGWUJKMDMyTFA1eWVTL1pwMTdGRzdpd3RTTXpoSVUybFgwWQp1K3RYNnJka2ZKNzgxaS8vanRzcWlIMUgvWkdxMENIbjNCclV3MFJOVi95dGZyZldSSmF5K3V4K0h6cER1S016Ck1acGtGRHYxUlNYbWlNcEFncStGaFpzRjg3Q0RIU2xNbGZIUzZndGp4ckJRbzdaVmpBdWVjdUs2VnNhVFlKUU4KTzZ0Q3B3dnhuMnVvNk56UnQ0NXNJVmxIV25NbHovYlNRMDFvbWJWQ2JXbE0xb29OZEplQUhZa2M0citOYUtjSApkZ0FYTitGS3lGY0RxZG5mSTgwSSt3Qm1GT1pxT0FFeExRS2pISzQrYVl6cG1uZWM5b0dGTVVhNXhjQklxZXNYCkptQ2E2bWxkZVN1QVBiZmhJQTBFRDFHdXdocFRDWjZyTUlURkxnUEd2dTdCN3FGMjZZczBJQ2VSWTRjbFgzbW8KMkNrTnFFY3JWcllTZ1hSN3A4ZXJVM1F0RUJUR1VaZ0UwOGFQclMyQjJzNUgyREtSNHI5NkJ3TzhBTUZMQnMzegppVHdGVXB5VVJqYWhwb0hDRGEwV0JaNTNXdnNTYkxLdXpmdVhSMzdHa1pEYkRmTFAvS1ZYOVV4WUdWaHZUVTE5CjZnWnd0alVlCj1zaWdxCi0tLS0tRU5EIFBHUCBTSUdOQVRVUkUtLS0tLQo=
remote: export GIT_OBJECT_DIRECTORY=/home/markomackic/Desktop/Workspace/peers/a/.git/./objects/incoming-AK24Oc
remote: export GIT_EXEC_PATH=/usr/lib/git-core
remote: export GIT_ASKPASS=/snap/code/111/usr/share/code/resources/app/extensions/git/dist/askpass.sh
remote: export GIT_PUSH_OPTION_COUNT=1
remote: export GIT_ALTERNATE_OBJECT_DIRECTORIES=/home/markomackic/Desktop/Workspace/peers/a/.git/./objects
remote: Recieved 1 lines
remote: 0000000000000000000000000000000000000000 cd293a826c114f7e602c1e2cd5dead35e91e654b refs/heads/peers/server_b
remote: {}
```

It works, it works !

Why is it important:

Well the peer repo (in this example `b`, but could be any) syncs the changes with other peers
through a ref `peers/{peer_name}` of the repo it wants to sync its data with ( in this case `a`),
and since the refs are open ended ( e.g everyone can push to anything) it's important to be able
to verify who did the push.

You can also notice I've changed the pre-recv hook a bit, I've been fiddling with it, and here is
what it looks like now ( so `pre-receive.py` in `peers/a`):

```python    
# requires https://gnupg.readthedocs.io/en/latest/

import os
import sys
import time
import subprocess
import tempfile
import json
import gnupg
import base64


def verify_push_signature(gpg_instance, signature_str, data_str):
    sign_file = tempfile.NamedTemporaryFile()
    sign_file.write(base64.b64decode(signature_str))
    sign_file.seek(0)    
    verified =  gpg_instance.verify_data(sign_file.name, data_str.encode('utf-8'))
    sign_file.close()
    return verified

# DSN -> decentralized social network
main_gpg_dir = os.environ.get('DSN_GPG_HOME', '../../../gpg/a/')
main_gpg_passphrase = os.environ.get('DSN_GPG_HOME', 'a_server')

assert os.path.isdir(main_gpg_dir)

gpg = gnupg.GPG(gnupghome=os.path.abspath(main_gpg_dir))

print(sys.argv, file=sys.stderr)

git_params={k:v for k,v in os.environ.items() if k.startswith("GIT_")}

for var, val in git_params.items():
    print("export %s=%s"%(var, val), file=sys.stderr)

git_push_opts = {v[0]:v[1] for v in [val.split(":") for k,val in os.environ.items() if k.startswith("GIT_PUSH_OPTION_")] if len(v) == 2}

assert "SIGNATURE" in git_push_opts

lines = sys.stdin.readlines();

print("Recieved %d lines"%(len(lines)))

assert len(lines) == 1

line = lines[0]

old, new, ref = line.rstrip().split()

print(old, new, ref)

ref_pts = ref.split("/")

assert len(ref_pts) == 4

_, _, t, who = ref_pts

assert t == 'peers' or t == 'users'    

if old != "0"*40: #since we pushed already we should already be in server keyring of this peer
    verified = verify_push_signature(gpg, git_push_opts['SIGNATURE'], new)
    print(verified.username)
    exit(1)

cmd = "git rev-list --pretty=oneline %s"

if old == "0"*40: #the creation of this ref probably
    cmd = cmd%(new)
else:
    cmd = cmd%("%s..%s"%(old, new))

rev_list = subprocess.run(cmd, shell=True, check=True, capture_output=True)

commits_incoming = reversed(rev_list.stdout.decode('utf-8').rstrip().splitlines())

# check what we have
rev_list_master_p = subprocess.run("git rev-list refs/heads/master", shell=True, capture_output=True)

commits_master = {k: True for k in rev_list_master_p.stdout.decode('utf-8').rstrip().splitlines()} if rev_list_master_p.returncode == 0 else {}

contains_add_server_sync = False

allowed_msgs = ["ADD_PEER"]

for c in commits_incoming:
    sha, message = c.split(" ", 2)
    
    if sha in commits_master:
        continue; # yeah we already have you, we don't care, if we already rebased ( means all checks passed)
    
    if not any([message.startswith(allowed) for allowed in allowed_msgs]):
        print("C_MSG '%s' doesn't obay the format"%message) # we'll see how to handle penalties 
        exit(1)

    sha_files = subprocess.run('git show --pretty="" --name-status %s'%sha, shell=True, check=True, capture_output=True).stdout.decode('utf-8').splitlines()

    # single file per commit ( only create !)
    assert len(sha_files) == 1
    
    fmode, fname = filter(lambda x: len(x) > 0, sha_files[0].split())

    # A: addition of a file
    assert fmode == 'A'

    # it's the same as the above (but doesn't show how the file influences previous state)
    sha_blobs = subprocess.run('git ls-tree -r %s'%sha, shell=True, check=True, capture_output=True).stdout.decode('utf-8').splitlines()

    assert len(sha_blobs) == 1

    _, _, blob_sha, _ = filter(lambda x: len(x) > 0, sha_blobs[0].split())

    print(fname)

    if message.startswith('ADD_PEER'): #isolation to functions will come later, as we implement more commands
        pts = message.split('/')
        
        # only server name as param
        assert len(pts) == 2

        _, server_name = pts
        
        assert fname == 'peer_repos/%s.json'%server_name 

        server_json = json.loads(subprocess.run('git cat-file -p %s'%blob_sha, shell=True, check=True, capture_output=True).stdout.decode('utf-8'))

        assert 'server_name' in server_json
        assert 'server_mail' in server_json
        assert 'server_repo' in server_json
        assert 'pubkey' in server_json

        assert server_json['server_name'] == server_name

        import_result = gpg.import_keys(base64.b64decode(server_json['pubkey'].encode('utf-8')).decode('utf-8'))

        print(dir(import_result), import_result.summary(), import_result.fingerprints)

        # now that we have successfully imported the key, let's sing it locally 

        assert len(import_result.fingerprints) == 1

        keysign = subprocess.run(
            'gpg --batch --yes --pinentry-mode loopback --passphrase $GPG_PASSPHRASE --lsign-key %s'%import_result.fingerprints[0],
            check=True,
            capture_output=True,
            shell=True,
            env = { 
                'GNUPGHOME': main_gpg_dir,
                'GPG_PASSPHRASE': main_gpg_passphrase 
            }
        )
        
        print("Summary : %s"%import_result.summary())
        print("Signing output stdout: %s"%keysign.stdout.decode('utf-8'))
        print("Signing output stderr: %s"%keysign.stderr.decode('utf-8'))


verified = verify_push_signature(gpg, git_push_opts['SIGNATURE'], new)

assert verified.username.startswith(who)

exit(0)
```

And now finally ( of course we'll remove those prints, but we have a long way to go)
we have ADD_PEER basically up and running. Let's try it:

```
markomackic@m3o:~/Desktop/Workspace/peers/b$ git push --push-option SIGNATURE:$(cat .git/refs/heads/master | tr -d "\n" | GNUPGHOME=../../gpg/b gpg --batch --pinentry-mode loopback --passphrase b_server -o - --armor --detach-sign 2>/dev/null | base64 -w 0) --set-upstream a master:peers/b_server
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 8 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (4/4), 3.21 KiB | 3.21 MiB/s, done.
Total 4 (delta 0), reused 4 (delta 0)
remote: ['hooks/../../pre_receive.py']
remote: export GIT_DIR=.
remote: export GIT_QUARANTINE_PATH=/home/markomackic/Desktop/Workspace/peers/a/.git/./objects/incoming-ueYk9y
remote: export GIT_PUSH_OPTION_0=SIGNATURE:LS0tLS1CRUdJTiBQR1AgU0lHTkFUVVJFLS0tLS0KCmlRR3pCQUFCQ2dBZEZpRUUrK2haZThURmo2d0I0SS9rOXprZHI1K0xjUFVGQW1OZ1FhY0FDZ2tROXprZHI1K0wKY1BYYUtRd0FrYUJoU2I1SU9mNk5TRnlJMFlGWGI1bXNucTVZcDFYYzlJZ3ljYXVVT0VoY0dJM2pkdGoxQUR6UAp1QmJkQlh3Ti82NVU0dnhrWmwzV0tWcHRRd0czaHMxeFp6WlFBYTBYTnVmQ3ZkOXdOVXFCM05KSFl2WmFDd0NFCi9CYkxSRzlFRytVZTIwYmhpa1JsSHFmZGdlZXVkVU9MaTR3dHliTkJtbG5xNTdVRnFXMlNsbnA2R0dNV3o0NUsKTnRzbkVXQmhEWlR3ck9IQjhjOUNPWCtpL00zcExTR2xaZitlR01xRXljQTB6enpDdzhFRkVRZ0xtYTAzY3hjaApHb3ZuTkRlWDNYOTU0UUxrcnNYZ1BwaFY0Yi9taVpwbytjbmdzMVZWeXZ1TENBSS9xem1ya2FVS20vVk1HSGh4Cld0aXRWaXE0cFY4SWRpSnNoR0cwSnYyV2cxQkdNQzl5eUVIUXljNlhDUkFML1JOVW9MNmZvU0dSMExDcGd0NXAKK2FGd0YrZ2xhbjVKTnpHaklJVGoyNmlkNkthOHZBZVBtMGdGOGZVWlQrM1lwazJsMHVJQUpZTk5rSnpFWVBFbwp1YUZ5Y0d6SWx6K1RERWdyR01yTkNraHJnekgwRjNWM01RbjVieDJWYTM0bnNFZ09IZTIxVUlMUjBmbGNYUVFzCnp5Y2t1T3AwCj1rYjJYCi0tLS0tRU5EIFBHUCBTSUdOQVRVUkUtLS0tLQo=
remote: export GIT_OBJECT_DIRECTORY=/home/markomackic/Desktop/Workspace/peers/a/.git/./objects/incoming-ueYk9y
remote: export GIT_EXEC_PATH=/usr/lib/git-core
remote: export GIT_ASKPASS=/snap/code/111/usr/share/code/resources/app/extensions/git/dist/askpass.sh
remote: export GIT_PUSH_OPTION_COUNT=1
remote: export GIT_ALTERNATE_OBJECT_DIRECTORIES=/home/markomackic/Desktop/Workspace/peers/a/.git/./objects
remote: Recieved 1 lines
remote: 0000000000000000000000000000000000000000 cd293a826c114f7e602c1e2cd5dead35e91e654b refs/heads/peers/b_server
remote: peer_repos/b_server.json
remote: ['__bool__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'count', 'counts', 'data', 'fingerprints', 'gpg', 'handle_status', 'imported', 'imported_rsa', 'n_revoc', 'n_sigs', 'n_subk', 'n_uids', 'no_user_id', 'not_imported', 'ok_reason', 'problem_reason', 'results', 'returncode', 'sec_dups', 'sec_imported', 'sec_read', 'stderr', 'summary', 'unchanged'] 0 imported ['FBE8597BC4C58FAC01E08FE4F7391DAF9F8B70F5']
remote: Summary : 0 imported
remote: Signing output stdout: 
remote: Signing output stderr: gpg: WARNING: unsafe permissions on homedir '/home/markomackic/Desktop/Workspace/peers/a/.git/../../../gpg/a'
remote: 
remote: pub  rsa3072/F7391DAF9F8B70F5
remote:      created: 2022-10-27  expires: 2024-10-26  usage: SC  
remote:      trust: unknown       validity: full
remote: sub  rsa3072/0A35484BD89B6980
remote:      created: 2022-10-27  expires: 2024-10-26  usage: E   
remote: [  full  ] (1). b_server <b_server@b_server>
remote: 
remote: "b_server <b_server@b_server>" was already locally signed by key 55D3D067984819DC
remote: Nothing to sign with key 55D3D067984819DC
remote: 
remote: Key not changed so no update needed.
remote: 
To ../a/
 * [new branch]      master -> peers/b_server
Branch 'master' set up to track remote branch 'peers/b_server' from 'a'.
markomackic@m3o:~/Desktop/Workspace/peers/b$     
```


### Today's session progress

Well we've gone the long way ! We have successfully implemented the pre-recv hook for ADD_PEER functionality,
now we're going to talk rebasing and distribution among other nodes ( actually no clue yet, but that is 
what I planned ). This is gonna be awasome. Stay tuned ! 

### Resources 

* [https://gnupg.org/documentation/manuals/gnupg.pdf](https://gnupg.org/documentation/manuals/gnupg.pdf)
* [https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)
  * We can sign individual commits ( very important for our usecase)
* [https://gnupg.readthedocs.io/en/latest/](https://gnupg.readthedocs.io/en/latest/)

### Music for concentration

* [https://www.youtube.com/watch?v=vCo-FptSP3c](https://www.youtube.com/watch?v=vCo-FptSP3c)

### Chapters

* [Chapter 1]({% post_url 2022-10-26-decentralized-git-social-network %})
* [Chapter 2]({% post_url 2022-10-27-decentralized-git-social-network %})
* [Chapter 3 - Me]({% post_url 2022-10-30-decentralized-git-social-network %})
