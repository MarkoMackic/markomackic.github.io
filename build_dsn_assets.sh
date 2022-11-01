ls _includes/dsn_series/externals/ | grep -v empty | xargs -I{} rm _includes/dsn_series/externals/{}

curl https://raw.githubusercontent.com/MarkoMackic/dsn/ffd925fe155f237aae969718c84f3bb0c1c2ffcb/pre_receive.py > _includes/dsn_series/externals/pre_receive-ffd925fe155f237aae969718c84f3bb0c1c2ffcb.py
