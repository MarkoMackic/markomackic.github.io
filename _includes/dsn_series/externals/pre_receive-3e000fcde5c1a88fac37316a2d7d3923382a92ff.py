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
main_gpg_passphrase = os.environ.get('DSN_GPG_PASSPHRASE', 'a_server')

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
