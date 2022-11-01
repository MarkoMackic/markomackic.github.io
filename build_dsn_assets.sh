ls _includes/dsn_series/externals/ | grep -v empty | xargs -I{} rm _includes/dsn_series/externals/{}

curl https://raw.githubusercontent.com/MarkoMackic/dsn/3e000fcde5c1a88fac37316a2d7d3923382a92ff/pre_receive.py > _includes/dsn_series/externals/pre_receive-3e000fcde5c1a88fac37316a2d7d3923382a92ff.py
